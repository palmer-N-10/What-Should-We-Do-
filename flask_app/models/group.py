from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import user_min
from flask_app.models import city

DATABASE = 'popsicle_jar'
TABLE1 = 's'

debug = True

class Group:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        if 'city_id' in data:
            location = Group.getCity(data['city_id']) # not city_id, query for full name
            self.city = location.city
            self.state = location.state
        self.users = []

    # ! Many To One, skip otherwise
    @classmethod
    def get_group_with_users( cls , data:dict ) -> object:
        query = """SELECT popsicle_jar.groups.*, users.id, CONCAT_WS(' ', first_name, last_name) AS name
                FROM group_members
                JOIN popsicle_jar.groups
                ON group_members.group_id = popsicle_jar.groups.id
                JOIN users
                ON group_members.user_id = users.id
                WHERE popsicle_jar.groups.id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db( query , data )
        group = cls( results[0] )
        if debug:
            print(results[0])
            print(f"Results: {results}")
        if not results[0]['first_namme']:
            return user
        for data in results:
            user_data= {
                'id' : data['id'],
                'name' : data['name']
            }
            group.users.append( user_min.User_Min( data ) )
        return group

    @staticmethod
    def getCity(zipcode: int) -> object:
        data = { 'zipcode' : zipcode }
        return city.City.get_one_by_zip(data)
        