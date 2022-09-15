from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import city
from flask import flash
from datetime import datetime
import re

DATABASE = 'popsicle_jar'
TABLE1 = 'events'
TABLE2 = 'users'

debug = True

class Event:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.name = data['name']
        self.when = Event.convertWhen(data['when'])
        if 'city_id' in data:
            location = Event.getCity(data['city_id'])
            self.city = location.city
            self.state = location.state
        self.twentyOnePlus = data['twentyOnePlus']
        self.description = data['description']
        self.activity_type = Event.getType(data['activity_id'])
        self.creator_id = data['creator_id'] # ROUTE NEEDS TO CONVERT TO NAME
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.many = []

    @classmethod
    def get_one(cls, data:dict) -> object or bool:
        query = f"SELECT * FROM {TABLE1} WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0]) if result else False

    @staticmethod
    def getType(act_id: int) -> str:
        query = "SELECT name FROM activities WHERE id = %(id)s;"
        data = { 'id' : act_id}
        activity = connectToMySQL(DATABASE).query_db(query, data)
        return activity or "No activity found"
    
    @staticmethod
    def convertWhen(time) -> str:
        return time.strftime("%d %B, %Y")

    @staticmethod
    def getCity(city_id: int) -> object:
        data = {"id" : city_id}
        return city.City.getOne(data)
        