

import os, logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData 
app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b40c078d12ec4b:c47aae51@us-cdbr-east-05.cleardb.net/heroku_f96716167ae3b98'

##class Game(db.Model):
##    __tablename__ = 'nba'
##    Q1 = db.Column(db.Integer)
##    Q2 = db.Column(db.Integer)
##    H = db.Column(db.Integer)
##    Q3 = db.Column(db.Integer)
##    Q4 = db.Column(db.Integer)
##    FG = db.Column(db.Integer)

@app.route('/')
def hello():
    #logging.basicConfig(filename='error.log',level=logging.DEBUG)

    #sess = db.create_engine('mysql://b40c078d12ec4b:c47aae51@us-cdbr-east-05.cleardb.net/heroku_f96716167ae3b98')
    #myconn = db.connect()
    result = db.engine.execute( '''select 2Q from nba where 1Q=45 and fg=205''')
    result = result.fetchone()
    for row in result:
        return str(row)
    
    #return 'hello world'
    #engine = create_engine('mysql://b40c078d12ec4b:c47aae51@us-cdbr-east-05.cleardb.net/heroku_f96716167ae3b98')
    #conn = engine.connect()
    #result = conn.execute('select * from nba')
    #for row in result:
        #return row
    
    #return conn
##    myNba = SQLAlchemy.Table('nba', metadata,
##                             SQLAlchemy.Column('1Q', Integer),
##                             SQLAlchemy.Column('2Q', Integer),
##                             SQLAlchemy.Column('H', Integer),
##                             SQLAhchemy.Column('3Q', Integer),
##                             SQLAlchemy.Column('4Q', Integer),
##                             SQLAlchemy.Column('FG', Integer)
##                             )
    
    #return 'Hello World!111'


