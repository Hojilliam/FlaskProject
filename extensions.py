from flask_sqlalchemy import SQLAlchemy
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

db = SQLAlchemy()

uri = 'mongodb+srv://jordan:kimov@cluster0.xrgey.mongodb.net/'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

