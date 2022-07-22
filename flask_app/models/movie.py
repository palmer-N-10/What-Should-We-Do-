from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
import requests, json

DATABASE = 'poogle'
class Movie:
    def __init__( self , data ):
        self.id = data['id']
        self.genre = data['genre']
        self.platform = data['platform']
        self.user_id = data['user_id']