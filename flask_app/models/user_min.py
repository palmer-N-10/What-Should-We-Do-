from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

DATABASE = 'popsicle_jar'
TABLE1 = 'users'

debug = True

class User_Min:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']