from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
import requests, json

DATABASE = 'poogle'
class Sport:
    def __init__( self , data ):
        self.id = data['id']
        self.team1 = data['team1']
        self.team2 = data['team2']
        self.team3 = data['team3']
        self.user_id = data['user_id']