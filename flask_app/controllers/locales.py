from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.locale import Locale

@app.route('/local')
def loc():
    if 'user_id' not in session:
        return redirect('/logout')
    x= Locale.get_traffic(session['lat'],session['lon'])
    y= Locale.get_weather(session['lat'],session['lon'])
    return render_template("local.html",x=x, y=y)