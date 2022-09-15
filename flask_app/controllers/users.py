from flask import render_template, redirect, request
from flask_app import app, Bcrypt, flash, session
from flask_app.models.user import User


## Toggle to run all debug statements to track data flow
## True = On, False = Off
debug = True

bcrypt = Bcrypt(app)

# # Root
@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect('/dashboard')
    return render_template('login_reg.html')

# # Register
@app.route('/register/create', methods=['POST'])
def create():
    if debug:
        print(f"Request Form dict: {request.form}")
    if not User.validate_model(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    if debug:
        print(f"Password Hash: {pw_hash}")
    # Ensure data keys are correct
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    if debug:
        print(f"Registration data dict: {data}")
    user_id = User.save(data)
    # Add user to session
    session['user_id'] = user_id
    session['first_name'] = data['first_name']
    session['logged_in'] = True
    # ! Auto login after registration, go to dashboard? main page?
    return redirect('/dashboard')

# # Login
@app.route('/login', methods=['POST'])
def login():
    data = { 'email' : request.form['email'] }
    user = User.get_by_col(data)
    if debug:
        print(f"Request Form dict: {request.form}")
        print(f"Hashed password: {user.password}")
        print(f"Entered password: {request.form['password']}")

    if not ( User.valid_email_format(data) and User.email_in_db(data) ):
        # De Morgans Law:
        # not (A and B) == (not A) or (not B)
        flash("Invalid credentials", "login")
        return redirect('/')
    elif not bcrypt.check_password_hash(user.password, request.form['password']):
        # check pw (hashed, unhashed)
        flash("Invalid credentials", "login")
        return redirect('/')
    else:
        session['user_id'] = user.id
        session['first_name'] = user.first_name
        session['logged_in'] = True
        return redirect('/dashboard')

# # Landing Page / Dashboard / Logged In
@app.route('/dashboard')
def success():
    if debug:
        print(f"Session while attempting to access success: {session}")
    if not 'logged_in' in session:
        flash("Please login before continuining.", "login")
        return redirect ('/')

    recipes = Recipe.get_all()
    # if debug:
    #     print(f"dashboard user data: {user}")
    #     print(f"User name: {user.first_name}")
    #     print(f"User recipes: {user.recipes[0].user_id}, {session['user_id']}")
    return render_template("dashboard.html", recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    if debug:
        print(f"Session after clear: {session}")
    return redirect('/')

@app.errorhandler(404)
def fourZeroFour(err):
    return "<h1 style='margin:50px auto; color:red'>Sorry!\
            No response. Try another address, ya dingus.</h1>"