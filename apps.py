import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import MySQLdb.cursors

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLACHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/fintech'

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'fintech',
) 

my_cursor = mydb.cursor()



