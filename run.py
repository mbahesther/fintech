from datetime import timedelta
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import MySQLdb.cursors

from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user



app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLACHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/fintech'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] =timedelta(hours=2)

jwt = JWTManager(app)
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'fintech',
) 

my_cursor = mydb.cursor()


my_cursor.execute( '''CREATE TABLE IF NOT EXISTS register (
	id INT(11) NOT NULL AUTO_INCREMENT,
	fullname	VARCHAR(50) NOT NULL,
	email	VARCHAR(120) NOT NULL,
	password	VARCHAR(200) NOT NULL,
    transaction_pin VARCHAR(200) NOT NULL,
    balance INT(200)  NOT NULL,
	PRIMARY KEY(id),
	UNIQUE(email)
)
''')
mydb.commit()


my_cursor.execute( '''CREATE TABLE IF NOT EXISTS transactions (
	trans_id INT(11) NOT NULL AUTO_INCREMENT,
	email	VARCHAR(120) NOT NULL,
    amount INT(200)  NOT NULL,
    type VARCHAR(20) NOT NULL,
    date VARCHAR(120) NOT NULL,
	PRIMARY KEY(trans_id),
	UNIQUE(email)
)
''')
mydb.commit()


