from flask import request, redirect, render_template,session, flash
from flask_app import app
from flask_app.models.patient import Patient
from flask_app.models.session import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/patient/create", methods = ['POST'])
def create_patient():
    if not Patient.validate_patient(request.form):
        return redirect("/patient/register")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'mail': request.form['mail'],
        'password': pw_hash
    }

    user_id = User.save_user(data)
    pat_data = {
        'dx': request.form['dx'],
        'birthday': request.form['birthday'],
        'amount' : request.form['amount'],
        'user_id' :user_id
    }
    patient_id = Patient.save_patient(pat_data)

    flash("Usuario creado, gracias! :)", "register")
    session['patient_id'] = patient_id 
    return redirect("/patient/register")

# Renderiza pagina de login/register
@app.route("/patient/register")
def form_patient():
    return render_template("registerpat.html")

# Procesamiento de login
@app.route ("/patient/login", methods = ['POST'])
def login_patient():
    data = {
        "mail" : request.form["mail"]
    }
    patient_db = Patient.get_login(data)
    if not patient_db:
        flash("Invalid mail/password", "login")
        return redirect("/patient/register")

    if not bcrypt.check_password_hash(patient_db.password, request.form['password']):
        flash("Invalid mail/password", "login")
        return redirect("/patient/register")
    
    session['patient_id'] = patient_db.id
    return redirect("/patient/dashboard")

##Dashboard o perfil con info del doctor
@app.route("/patient/dashboard")
def dash_patient():
    return render_template("dashpatient.html")


