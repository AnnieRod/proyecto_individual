from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask import flash

## Clase de usuario para poder heredar en las otras tablas
class User:
    data_name = "medcenter"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.mail = data['mail']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, mail, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(mail)s, %(password)s, NOW(), NOW());"
        user = connectToMySQL(cls.data_name).query_db(query, data)
        return user

##clase de citas para info recibida de form
class Session: 
    data_name = "medcenter"
    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.hour = data['hour']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.doctor_id = data['doctor_id']
        self.patient_id = data['patient_id']
        self.area_id = data['area_id']

    @classmethod
    def make_appointment(cls,data):
        query = "INSERT INTO sessions (date, hour, created_at, updated_at, doctor_id, patient_id, area_id) VALUES (%(date)s, %(hour)s, NOW(), NOW(), %(doctor_id)s, %(patient_id)s, %(area_id)s);"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        return result 
    
    @staticmethod
    def validate_appointment(appointment):
        is_valid = True
        today_date = datetime.today().strftime('%Y-%m-%d')
        if appointment["date"] == "":
            flash("Debes seleccionar una fecha", "register")
            is_valid = False
        if appointment["date"] < today_date:
            flash("Selecciona una fecha valida", "register")
            is_valid = False
        if appointment["hour"] == "":
            flash("Debes seleccionar una hora", "register")
            is_valid = False
        # if appointment["hour"] > 15:   ARREGLA ESTO, COMO PONER LIMITE DE HORA
        #     flash("Recuerda que la ultima cita programable es hasta las 3pm", "register")
        #     is_valid = False
        if appointment["doctor_id"] == "":
            flash("Debes seleccionar un doctor", "register")
            is_valid = False
        if appointment["area_id"] == "":
            flash("Debes seleccionar un servicio", "register")
        ##Valida si doctor SI pertenece al área seleccionada: ARREGLA ESO, CONSULTA VA BIEN PERO ACÁ NO  FUNCIONA
        # query = "SELECT * FROM doctors WHERE doctors.id NOT IN (SELECT doctors.area_id FROM doctors LEFT JOIN areas ON areas.id = doctors.area_id WHERE areas.id = %(area_id)s)"
        # coincidence = connectToMySQL("medcenter").query_db(query, appointment)
        # if len(coincidence) >= 1:
        #     flash ("El doctor no pertenece a esa area", "register")
        #     is_valid = False
        #     return is_valid
        return is_valid