from mongoengine import Document, StringField, DateTimeField,BooleanField
import datetime
 
class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)  # Store hashed passwords
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    is_author = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    is_user = BooleanField(default=True)
 
    meta = {
        'collection': 'User'  # Specify the collection name
    }