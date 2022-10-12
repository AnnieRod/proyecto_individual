from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.session import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Doctor(User):
    data_name = "medcenter"
    def __init__(self, data):
        super().__init__(data)
        self.id = data['id']
        self.card = data['card']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.area_id = data['area_id']
        self.user_id = data['user_id'] ##está bien esto aca?

    @classmethod
    def save_doctor(cls, data):
        query = "INSERT INTO doctors(card, created_at, updated_at, area_id, user_id) VALUES (%(card)s, NOW(), NOW(), %(area_id)s, %(user_id)s);"
        doctor = connectToMySQL(cls.data_name).query_db(query, data)
        return doctor

    @classmethod
    def get_doctor(cls, data):
        query = "SELECT * FROM doctors WHERE id = %(id)s;"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all_doctors(cls): ##Aun no funciona, key errors diferentes
        query = "SELECT doctors.*,users.first_name, users.last_name, users.mail, users.password FROM doctors JOIN users ON users.id = doctors.user_id;"
        results = connectToMySQL(cls.data_name).query_db(query)
        all_doctors = []
        for doctor in results:
            all_doctors.append(cls(doctor))
        return all_doctors

    ##revisa si correo coincide para iniciar sesión y luego valida datos
    @classmethod
    def get_login(cls, data):
        query = "SELECT * FROM doctors JOIN users ON users.id = doctors.user_id WHERE mail =%(mail)s;"
        result = connectToMySQL(cls.data_name).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_doctor(doctor): ##Mira si puedes heredar esto
        is_valid = True
        if len(doctor["first_name"]) < 2:   ##pendiente que solo sea letras
            flash("Tu nombre debe tener al menos dos caracteres.", "register")
            is_valid = False
        if len(doctor["last_name"]) < 2:   ##pendiente que solo sea letras
            flash("Tu apellido debe tener al menos dos caracteres.", "register")
            is_valid = False
        ##Valida que el correo no este registrado ya
        query = "SELECT * FROM doctors JOIN users ON users.id = doctors.user_id WHERE mail =%(mail)s;"
        coincidence = connectToMySQL("medcenter").query_db(query, doctor)
        if len(coincidence) >= 1:
            flash ("Email no valido, ya está registrado", "register")
            is_valid = False
            return is_valid
        if not EMAIL_REGEX.match(doctor['mail']):
            flash("Email no valido", "register")
            is_valid = False
        if len(doctor["password"]) < 8: 
            flash("La contraseña debe tener al menos 8 caracteres.", "register")
            is_valid = False
        if doctor["password"] != doctor['confirm_password']:
            flash("Las contraseñas no coinciden", "register")
            is_valid = False
        if len(doctor["card"]) < 4: 
            flash("Tu registro profesional debe ser más largo", "register")
            is_valid = False
        if doctor["area_id"] == "":
            flash("Debes seleccionar un servicio", "register")
            is_valid = False
        return is_valid