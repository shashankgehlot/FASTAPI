from mongoengine import Document, EmbeddedDocument, StringField, ReferenceField, ListField, DateTimeField, EmbeddedDocumentField,UUIDField,ImageField
from authenticator.models import User
from datetime import datetime
from slugify import slugify

import uuid
 
 
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

class Tags(Document):
    title = StringField(required=True)


class Post(Document):
    title = StringField(required=True, unique=True)
    content = StringField(required=True)
    author = ReferenceField(Author, required=True)
    comments = ListField(EmbeddedDocumentField(Comment), default=list)
    tags = ListField(ReferenceField(Tags), default=list ,required=False)  # Corrected field definition
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    slug_title = StringField(unique=False)
    thumbnail_base64 = StringField(required=False)
    post_image_base64 = StringField(required=False)

    

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

    def delete_comment(self, comment_id):
        """Method to delete an existing comment."""
        for comment in self.comments:
            if comment.id == comment_id:
                self.comments.remove(comment)
                break
        self.save()  # Save the post with the updated comment

    
    def add_tags(self, title):
        """Method to add a new tag to the post."""
        try:
            tag = Tags.objects.get(title=title)
        except Tags.DoesNotExist:
            tag = Tags(title=title).save()
        if tag not in self.tags:
            self.tags.append(tag)
        self.save()  # Save the post with the new tag

    def remove_tags(self, title):
        """Method to remove a tag from the post."""
        try:
            tag = Tags.objects.get(title=title)
            if tag in self.tags:
                self.tags.remove(tag)
                self.save()  # Save the post with the tag removed
        except Tags.DoesNotExist:
            pass  # Tag does not exist, nothing to remove

    def update_tag(self, old_title, new_title):
        """Method to update an existing tag's title."""
        try:
            tag = Tags.objects.get(title=old_title)
            if tag in self.tags:
                tag.title = new_title
                tag.save()  # Save the updated tag
                self.save()  # Save the post with the updated tag
        except Tags.DoesNotExist:
            pass  # Tag with old_title does not exist

    def set_thumbnail(self, thumbnail_base64):
        """Method to set the thumbnail image in base64 format."""
        self.thumbnail_base64 = thumbnail_base64
        self.save()  # Save the post with the new thumbnail

    def set_post_image(self, post_image_base64):
        """Method to set the post image in base64 format."""
        self.post_image_base64 = post_image_base64
        self.save()  # Save the post with the new image
