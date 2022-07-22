from flask import Flask, session, flash
from flask_bcrypt import Bcrypt
import re
import requests
app = Flask(__name__)


app.secret_key = "jon bones jones"

bcrypt = Bcrypt(app)