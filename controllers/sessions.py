from flask import request, redirect, render_template,session, flash
from flask_app import app
from flask_app.models.area import Area
from flask_app.models.doctor import Doctor
from flask_app.models.session import Session

## Todo lo relacionado con la pagina de crear cita, citas y con la pagina de servicios
@app.route("/services")
def services_appointment():
    return render_template("services.html") #agrega funciones para mostrar nombre y demas de paciente

@app.route("/patient/takesession")   ##esto va en el boton de pedir cita por servicio
def program_session():
    if 'patient_id' not in session:
        return redirect("/patient/register")
    return render_template("sessions.html", all_doctors = Doctor.get_all_doctors(), all_areas = Area.load_area()) #agrega funciones para mostrar nombre y demas de paciente


@app.route("/patient/programsession", methods = ['POST'])
def create_appointment():
    if 'patient_id' not in session:
        return redirect("/patient/register")
    if not Session.validate_appointment(request.form):
        return redirect("/patient/takesession")

    data = {
        'date': request.form['date'],
        'hour': request.form['hour'],
        'doctor_id': request.form['doctor_id'],
        'area_id' : request.form['area_id'],
        'patient_id' : session['patient_id'],
    }

    Session.make_appointment(data)
    flash("Usuario creado, gracias! :)", "register")
    return redirect("/patient/dashboard")