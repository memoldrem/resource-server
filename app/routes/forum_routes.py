from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

app = Flask(__name__)


load_dotenv()

# PostgreSQL Config
database_url = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)

# MongoDB Config
mongo_db = os.getenv('MONGO_URI') 
mongo = PyMongo(app)

