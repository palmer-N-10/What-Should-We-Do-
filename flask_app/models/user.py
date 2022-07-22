from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
import requests, json


DATABASE = 'poogle'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.ip = data['ip']
        self.longitude = data['longitude']
        self.latitude = data['latitude']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password,ip,longitude,latitude) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s,%(ip)s,%(longitude)s,%(latitude)s);"
        return connectToMySQL(DATABASE).query_db( query, data )
    
    @classmethod
    def get_by_email(cls,data:dict) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def get_location_data(cls,data:dict) -> object or bool:
        query = "SELECT users.longitude,users.latitude FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        kobe=[cls(result[0])]
        return kobe

    
    @classmethod
    def update_local(cls,data:dict) -> int:
        query = "UPDATE users SET ip=%(ip)s,longitude=%(longitude)s,latitude=%(latitude)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    
    @staticmethod
    def get_ip():
        response = requests.get('https://api64.ipify.org?format=json').json()
        return response["ip"]

    @staticmethod
    def get_location(ip_address):
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        location_data = {
            "ip": ip_address,
            "longitude": response.get("longitude"),
            "latitude": response.get("latitude"),
        }
        return location_data
    
    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True # ! we assume this is true
        if len(user['first_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(user['password']) != 8:
            flash("password must be 8 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if user['password'] != user['confirm-password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid

    