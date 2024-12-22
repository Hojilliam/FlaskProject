from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

db = SQLAlchemy()

uri = 'mongodb+srv://jordan:kimov@cluster0.xrgey.mongodb.net/'

# Create a new client and connect to the server
client = MongoClient(uri)

