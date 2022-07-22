from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
import requests, json

DATABASE = 'poogle'
class Crypto:
    def __init__( self , data ):
        self.id = data['id']
        self.ticker1 = data['ticker1']
        self.ticker2 = data['ticker2']
        self.ticker3 = data['ticker3']
        self.user_id = data['user_id']