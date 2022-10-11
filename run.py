import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import MySQLdb.cursors

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLACHEMY_DATABASE_URI'] = 'postgres://abdbydvidkxekc:f56796c4310c3ef6456fe376681d75c9e63aa1af103a43e887019907a5b63e98@ec2-3-213-66-35.compute-1.amazonaws.com:5432/d3cuo5olh7pkr4'
#app.config['SQLACHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/fintech'

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'fintech',
) 

my_cursor = mydb.cursor()

my_cursor.execute( '''CREATE TABLE IF NOT EXISTS user_register (
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

