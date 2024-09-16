from mongoengine import Document, StringField, DateTimeField
import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)  # Store hashed passwords
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'User'  # Specify the collection name
    }