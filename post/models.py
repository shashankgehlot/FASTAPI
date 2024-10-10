from mongoengine import Document, EmbeddedDocument, StringField, ReferenceField, ListField, DateTimeField, EmbeddedDocumentField,UUIDField
from authenticator.models import User
from datetime import datetime
import uuid
 
 
# Author model
class Author(Document):
    user = ReferenceField(User, required=True)
    bio = StringField()
 
    def __str__(self):
        return f"{self.user.username} (Author)"
 
class Comment(EmbeddedDocument):
    id = UUIDField(binary=False, default=uuid.uuid4, unique=True)
    content = StringField(required=True)
    author = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
 
class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    author = ReferenceField(Author, required=True)
    comments = ListField(EmbeddedDocumentField(Comment))
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
 
    meta = {'collection': 'Post'}
 
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Post, self).save(*args, **kwargs)
 
    def __str__(self):
        return self.title