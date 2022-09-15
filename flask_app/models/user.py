from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import sig_other
from flask_app.models import city
from flask_app.models import event
from flask_app.models import friend
from flask_app.models import user_group
from flask_app.models import group
from flask import flash
from datetime import datetime
import re

DATABASE = 'popsicle_jar'
TABLE1 = 'users'

debug = True

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.age  = User.getAge(data['birthday'])
        if 'city_id' in data:
            location = User.getCity(data['city']) # not city_id, query for full name
            self.city = location.city
            self.state = location.state
        self.birthday = data['birthday']
        self.password = data['password']
        self.avatar_num = data['avatar_num'] or 1
        # If valid connection has been accepted by this user
        if 'sig_other_id' in data:
            sig_other = User.getSigOther(data['sig_other_id'])
            self.sig_other_id = sig_other.id
            self.sig_other_name = sig_other.name
        # If a request has been made by someone else
        if 'sig_other_request_id' in data:
            self.sig_other_request_id = data['sig_other_request_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.friends = []
        self.groups = []
        self.events = []

    @classmethod
    def get_all(cls) -> list:
        query = f"SELECT * FROM {TABLE1};"
        results = connectToMySQL(DATABASE).query_db(query)
        user_list = []
        for user in results:
            user_list.append( cls(user) )
        return user_list

    @classmethod
    def get_one(cls, data:dict) -> object or bool:
        query = f"SELECT * FROM {TABLE1} WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0]) if result else False

    @staticmethod
    def getSigOther(sig_other_id: int) -> object:
        data = { 'id' : sig_other_id}
        return sig_other.Sig_Other.getSigOther(data)

    # ! Many To One, skip otherwise
    @classmethod
    def get_user_with_friends( cls , data:dict ) -> object:
        query = f"""SELECT u1.*, f1.id, CONCAT_WS(' ', f1.first_name, f1.last_name) as friend
                    FROM friends
                    JOIN users as u1
                    ON friends.user_id = u1.id
                    JOIN users as f1
                    ON friends.friend_id = f1.id
                    WHERE friends.user_id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db( query , data )
        user = cls( results[0] )
        if debug:
            print(results[0])
            print(f"Results: {results}")
        if not results[0]['f1.id']:
        # if no friends are found
            return user
        for data in results:
            friend_data= {
                "id" : data['f1.id'],
                "name" : data['friend']
            }
            user.friends.append( friend.Friend( data ) )
        return user
        

    # ! Many To One, skip otherwise
    @classmethod
    def get_user_with_groups( cls , data:dict ) -> object:
        query = """SELECT users.*, popsicle_jar.groups.name, popsicle_jar.groups.id
                    FROM users
                    JOIN group_members
                    ON group_members.user_id = users.id
                    JOIN popsicle_jar.groups
                    ON group_members.group_id = popsicle_jar.groups.id
                    WHERE users.id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db( query , data )
        user = cls( results[0] )
        if debug:
            print(results[0])
            print(f"Results: {results}")
        if not results[0]['name']:
            return user
        for data in results:
            friend_data= {
                "id" : data['groups.id'],
                "name" : data['name']
            }
            user.groups.append( user_group.User_Group( data ) )
        return user

    # ! Many To One, skip otherwise
    @classmethod
    def get_user_with_events( cls , data:dict ) -> object:
        query = """SELECT users.*, name, events.when, description, count(user_id) AS attending
                    FROM events_has_users
                    JOIN users
                    ON events_has_users.user_id = users.id
                    JOIN events
                    ON events_has_users.user_id = events.id
                    WHERE events_has_users.event_id = %(event_id)s;"""
        results = connectToMySQL(DATABASE).query_db( query , data )
        user = cls( results[0] )
        if debug:
            print(results[0])
            print(f"Results: {results}")
        for data in results:
            recipe_data= {
                "id" : data['recipes.id'],
                "name" : data['name'],
                "description" : data['description'],
                "instructions" : data['instructions'],
                "under_30" : data['under_30'],
                "origin_date" : data['origin_date'],
                "user_id" : data['user_id'],
                "created_at" : data['created_at'],
                "updated_at" : data['updated_at'],
            }
            ### CHANGE THIS TO INCLUDE CORRECT SECONDARY MODEL 
            user.recipes.append( recipe.Recipe( recipe_data ) )
            ### CHANGE THIS TO INCLUDE CORRECT SECONDARY MODEL 
        return user

    @staticmethod
    def getAge(birthdate) -> int:
        # https://www.codingem.com/how-to-calculate-age-in-python/
        # Get today's date object
        today = datetime.today()
        
        # A bool that represents if today's day/month precedes the birth day/month
        isThisYear = ((today.month, today.day) < (birthdate.month, birthdate.day))
        year_difference = today.year - birthdate.year
        
        # The difference in years is not enough. 
        # To get it right, subtract 1 or 0 based on if today precedes the 
        # birthdate's month/day.
        
        # To do this, subtract the 'isThisYear' boolean 
        # from 'year_difference'. (This converts
        # True to 1 and False to 0 under the hood.)
        age = year_difference - isThisYear
        return age
    
    @staticmethod
    def getCity(zipcode: int) -> object:
        data = { 'zipcode' : zipcode }
        return city.City.get_one_by_zip(data)


    @classmethod
    def validate_model(cls, user:dict) -> bool:
        is_valid = True
        if len(user['first_name']) < 2 or not user['first_name'].isalpha():
            if debug:
                print(f"First name: {user['first_name']}")
                print(f"First name length: {len(user['first_name'])}")
                print(f"First name isalpha: {user['first_name'].isalpha()} ")
            flash("First name must be at least 2 characters an only letters.")
            is_valid = False
        if len(user['last_name']) < 2 or not user['last_name'].isalpha():
            if debug:
                print(f"Last name: {user['last_name']}")
                print(f"Last name length: {len(user['last_name'])}")
                print(f"Last name isalpha: {user['last_name'].isalpha()} ")
            flash("Last name must be at least 2 characters an only letters.")
            is_valid = False
        if not cls.valid_email_format(user):
            flash("Invalid email address.")
            is_valid = False
        if cls.email_in_db(user):
            flash("Email in use already.")
            is_valid = False
        if not cls.valid_password(user):
            is_valid = False
        if len(user['zipcode']) < 3 or len(user['zipcode']) > 5:
            flash("US ZipCodes must be between 3 and 5 numbers, inclusive.")
            is_valid = False
        return is_valid

    @staticmethod
    def valid_email_format( data:dict ) -> bool:
        # create regex pattern
        regex = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
        match = re.search(regex, data['email'])
        if debug:
            print(f"Email: {data['email']}")
            print(match)
        return True if match else False

    @classmethod
    def email_in_db( cls, data: dict ) -> bool:
        users_emails = {user.email for user in cls.get_all()}
        # set comprehension, make a set (unique values) of all user emails
        # from the users in User.get_all()
        if debug:
            print(f"Users Email List: {users_emails}")
            print(f"User Email: {data['email']}")
        return True if data['email'] in users_emails else False

    # Made by person requesting to add email of significant other, adds a pending request to the signifncant other
    @classmethod
    def lookup_sig_other_email(cls,data:dict) -> bool:
        # Data should be:
        # user id
        # sig_other_email
        query = f"SELECT * FROM {TABLE1} WHERE email = %(sig_other_email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if result:
            # Swap data going to sig_other.
            # User data
            sig_other_data = {
                "sig_other_request_id" : data['sig_other_request_id'],
                'id' : result[0]['id']
                }
            cls.update_sig_other_request(sig_other_data)
            flash("S.O. Request has been made.")
            return True
        else:
            flash("Significant Others email not found in the database.")
            return False

    # Called  when user added/updated in datatbase, if they provided a valid email
    @staticmethod
    def update_sig_other_request(data) -> None:
        query = f"UPDATE {TABLE1} SET sig_other_request_id = %(id)s WHERE id = %(sig_other_request_id)s;"
        connectToMySQL(DATABASE).query_db( query, data )

    @staticmethod
    def valid_password(user:dict) -> bool:
        if debug:
            print("Starting password validation.")
        # Checks matching passwords, length, contains upper, lower and digit
        is_valid = True
        if debug:
            print(f"password: {user['password']}")
            print(f"password confirm: {user['password-confirm']}")
        if user['password'] != user['password-confirm']:
            flash("Passwords do not match.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long.", "register")
            is_valid = False
        
        hasUpper = hasLower = hasDigit = False
        charInd = 0
        while (not (hasUpper and hasLower and hasDigit)) and (charInd < len(user['password'])):
            if debug:
                print("Inside password while loop.")
            # while TRUE and TRUE
            # not (A and B and C) == (not A) or (not B) or (not C)
            # True or True or True == True or False or False == True
            if user['password'][charInd].isupper(): hasUpper = True
            if user['password'][charInd].islower(): hasLower = True
            if user['password'][charInd].isdigit(): hasDigit = True
            charInd += 1
        if debug:
            print("End password while loop")
        if not (hasUpper and hasLower and hasDigit):
            flash("Password must contain at least 1 lower character, 1 upper character and a digit.", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def save(data):
        query = f"""INSERT INTO {TABLE1}
                ( first_name, last_name, email, birthday, password )
                VALUES
                ( %(first_name)s, %(last_name)s, %(email)s, %(birthday)s %(password)s );"""
        return connectToMySQL(DATABASE).query_db( query, data )

    @staticmethod
    def del_one(data):
        query = f"DELETE FROM {TABLE1} WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @staticmethod
    def update(data):
        query = f"UPDATE {TABLE1} SET name = %(name)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db( query, data )
    
    @staticmethod
    def add_sig_other(data: dict) -> None:
        query = f"""UPDATE {TABLE1}
                SET sig_other_id = %(sig_other_id)s, sig_other_request_id = NULL
                WHERE id = %(id)s;"""
        connectToMySQL(DATABASE).query_db( query, data )