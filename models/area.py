from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.session import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Area:
    data_name = "medcenter"
    def __init__(self, data):
        self.id = data['id']
        self.area_name = data['area_name']

    @classmethod
    def load_area(cls):  
        query = "SELECT * FROM areas;"
        results = connectToMySQL(cls.data_name).query_db(query)
        all_areas = []
        for area in results:
            all_areas.append(cls(area))
        return all_areas
