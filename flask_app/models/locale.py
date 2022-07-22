from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from flask_app.models.user import User
import requests, json
DATABASE = 'poogle'

class Locale:
    def __init__( self , data ):
        self.ip = data['ip']
        self.longitude = data['longitude']
        self.latitude = data['latitude']

    @classmethod
    def get_location_data(cls,data:dict) -> object or bool:
        query = "SELECT users.longitude,users.latitude FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        kobe=[cls(result[0])]
        return kobe

    @classmethod
    def get_traffic(cls,lat,lon):
        key = "pmTWf3lDAmSIV7D7GLAOAmAeUNBYAUr4"
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}').json()
        return response

    @classmethod 
    def get_weather(cls,lat,lon):
        key = "cb79131241d470efaf3017d6a840b4b4"
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}').json()
        return response