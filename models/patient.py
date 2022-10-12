from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask_app.models.session import User
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Patient(User):
    data_name = "medcenter"
    def __init__(self, data):
        super().__init__(data)
        self.id = data['id']
        self.dx = data['dx']
        self.amount = data['amount']
        self.birthday = data['birthday']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id'] ##esta bien poner esto aca? 

    @classmethod
    def save_patient(cls, data):
        query = "INSERT INTO patients (dx, amount, birthday, created_at, updated_at, user_id) VALUES (%(dx)s, %(amount)s, %(birthday)s, NOW(), NOW(), %(user_id)s);"
        patient = connectToMySQL(cls.data_name).query_db(query, data)
        return patient

    @classmethod
    def get_patient(cls, data):
        query = "SELECT * FROM patients WHERE id = %(id)s;"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM patients;"
        results = connectToMySQL(cls.data_name).query_db(query)
        patients = []
        for patient in results:
            patients.append(cls(patient))
        return patients

    ##revisa si correo coincide para iniciar sesión y luego valida datos
    @classmethod
    def get_login(cls, data):
        query = "SELECT * FROM patients JOIN users ON users.id = patients.user_id WHERE mail =%(mail)s;"
        result = connectToMySQL(cls.data_name).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_patient(patient): ##Mira si puedes heredar esto
        is_valid = True
        today_date = datetime.today().strftime('%Y-%m-%d')
        if len(patient["first_name"]) < 2:   ##pendiente que solo sea letras
            flash("Tu nombre debe tener al menos dos caracteres.", "register")
            is_valid = False
        if len(patient["last_name"]) < 2:   ##pendiente que solo sea letras
            flash("Tu apellido debe tener al menos dos caracteres.", "register")
            is_valid = False
        ##Valida que el correo no este registrado ya
        query = "SELECT * FROM patients JOIN users ON users.id = patients.user_id WHERE mail =%(mail)s;"
        coincidence = connectToMySQL("medcenter").query_db(query, patient)
        if len(coincidence) >= 1:
            flash ("Email no valido, ya está registrado", "register")
            is_valid = False
            return is_valid
        if not EMAIL_REGEX.match(patient['mail']):
            flash("Email no valido", "register")
            is_valid = False
        if len(patient["password"]) < 8: 
            flash("La contraseña debe tener al menos 8 caracteres.", "register")
            is_valid = False
        if patient["password"] != patient['confirm_password']:
            flash("Contraseñas no coinciden", "register")
            is_valid = False
        if len(patient["dx"]) < 2:
            flash("Necesitas poner al menos las siglas del diagnóstico", "register")
            is_valid = False
        if len(patient["amount"]) < 1: 
            flash("Debes tener al menos una sesión aprobada para recibir nuestros servicios.", "register")
            is_valid = False  
        if patient["birthday"] == "":
            flash("Debes seleccionar una fecha", "register")
            is_valid = False
        if patient["birthday"] > today_date:
            flash("Selecciona una fecha valida", "register")
            is_valid = False
        return is_valid