from mongoengine import StringField, DateTimeField, Document,ReferenceField
from authenticator.models import User
import datetime
 
class Author(Document):
    user_id = ReferenceField(User, required=True)
    bio = StringField()
 
    meta = {
        'collection': 'Author'  # Specify the collection name
    }
 
class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    author = ReferenceField(Author, required=True)
 
    meta = {
        'collection': 'Post'  # Specify the collection name
    }
