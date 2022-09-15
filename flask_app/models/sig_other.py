from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

DATABASE = 'popsicle_jar'
TABLE1 = 'users'

debug = True

class Sig_Other:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']

    @classmethod
    def getSigOther(cls, data: dict) -> object:
        query = f"SELECT id, CONCAT_WS(' ', first_name, last_name) as name FROM {TABLE1} WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        # Validate in User init so no need to validate here (no else False)
        return cls(result[0])