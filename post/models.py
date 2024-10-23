from mongoengine import Document, EmbeddedDocument, StringField, ReferenceField, ListField, DateTimeField, EmbeddedDocumentField,UUIDField
from authenticator.models import User
from datetime import datetime
import uuid
from slugify import slugify

 
# Author model
class Author(Document):
    user = ReferenceField(User, required=True)
    bio = StringField()
 
    def __str__(self):
        return f"{self.user.username} (Author)"
 
class Comment(EmbeddedDocument):
    id = UUIDField(binary=False, default=uuid.uuid4)  # Keep it without unique=True
    content = StringField(required=True)
    author = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow)

class Post(Document):
    title = StringField(required=True,unique=True)
    content = StringField(required=True)
    author = ReferenceField(Author, required=True)
    comments = ListField(EmbeddedDocumentField(Comment), default=list)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    slug_title = StringField(unique=False)

    meta = {'collection': 'Post'}

    def save(self, *args, **kwargs):
        # Ensure all comments have a unique ID before saving
        for comment in self.comments:
            if comment.id is None:  # Check for None
                comment.id = uuid.uuid4()  # Assign a new UUID

        self.updated_at = datetime.utcnow()
        self.slug_title = slugify(self.title)

        # Call the parent save method
        return super(Post, self).save(*args, **kwargs)

    def add_comment(self, content, author):
        """Method to add a new comment to the post."""
        comment = Comment(content=content, author=author)
        self.comments.append(comment)
        self.save()  # Save the post with the new comment

    def update_comment(self, comment_id, new_content):
        """Method to update an existing comment."""
        for comment in self.comments:
            if comment.id == comment_id:
                comment.content = new_content
                break
        self.save()  # Save the post with the updated comment