

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b40c078d12ec4b:c47aae51@us-cdbr-east-05.cleardb.net/heroku_f96716167ae3b98'

@app.route('/')
def hello():
    return 'Hello World!111'


