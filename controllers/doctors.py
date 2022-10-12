from flask import request, redirect, render_template,session, flash

from flask_app import app
from flask_app.models.area import Area
from flask_app.models.doctor import Doctor

from flask_app.models.session import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

## Home
@app.route("/")
def start_app():
    return render_template("index.html")

## Pagina de contacto 
@app.route("/contact")
def show_info():
    return render_template("contact.html")

## Crea usuario de base para luego tomar su id y crear DOCTOR
@app.route("/doctor/create", methods = ['POST'])
def create_user():
    if not Doctor.validate_doctor(request.form):
        return redirect("/doctor/register")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'mail': request.form['mail'],
        'password': pw_hash
    }

    user_id = User.save_user(data)
    doc_data = {
        'card': request.form['card'],
        'area_id': request.form['area_id'],
        'user_id' :user_id
    }
    doctor_id = Doctor.save_doctor(doc_data)

    flash("Usuario creado, gracias! :)", "register")
    session['doctor_id'] = doctor_id 
    return redirect("/doctor/register")

# Renderiza pagina de login/register
@app.route("/doctor/register")
def form_doctor():
    return render_template("registerdoc.html", all_areas= Area.load_area())

# Procesamiento de login
@app.route ("/doctor/login", methods = ['POST'])
def login_doctor():
    data = {
        "mail" : request.form["mail"]
    }
    doctor_db = Doctor.get_login(data)
    if not doctor_db:
        flash("Invalid mail/password", "login")
        return redirect("/doctor/register")

    if not bcrypt.check_password_hash(doctor_db.password, request.form['password']):
        flash("Invalid mail/password", "login")
        return redirect("/doctor/register")
    
    session['doctor_id'] = doctor_db.id
    return redirect("/doctor/dashboard")

##Dashboard o perfil con info del doctor
@app.route("/doctor/dashboard")
def dash_doctor():
    return render_template("dashdoctor.html")