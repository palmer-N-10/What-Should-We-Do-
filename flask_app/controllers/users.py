from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.user import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def dash():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("got_you.html")

@app.route("/register/user", methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    ip = User.get_ip()
    location = User.get_location(ip)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash,
        "ip" : location['ip'],
        "longitude" : location['longitude'],
        "latitude" : location['latitude']
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session[ 'lon'] : location['longitude']
    session[ 'lat'] : location['latiude']
    return redirect('/home')

@app.route('/login', methods=['post'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('invalid credentials')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        return redirect('/')
    ip = User.get_ip()
    location = User.get_location(ip)
    data = {
        "id" :  session['user_id'],
        "ip" : location['ip'],
        "longitude" : location['longitude'],
        "latitude" : location['latitude']
    }
    User.update_local(data)
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    session['lon'] = location['longitude']
    session['lat'] = location['latitude']
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')




