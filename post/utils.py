from authenticator.models import User
from post.models import Author, Post
from post.schemas import AuthorCreate, PostCreate , UserResponseSchema,PostResponse
from typing import Optional
 
def get_user(user_id: str) -> Optional[UserResponseSchema]:
    user = User.objects(id=user_id).first()
    if user:
        return UserResponseSchema(id=str(user.id),username=user.username ,email=user.email)
    return None
 
def create_author(author: AuthorCreate):
    db_user = User.objects(id=author.user_id).first()
    if not db_user:
        return None
    db_author = Author(user_id=db_user, bio=author.bio)
    db_author.save()
    return db_author
 
def get_author(author_id: str):
    return Author.objects(id=author_id).first()
 
def create_post(post: PostCreate):
    db_author = get_author(post.author_id)
    if not db_author:
        return None
    db_post = Post(title=post.title, content=post.content, author=db_author)
    db_post.save()
    return db_post
 
def get_post(post_id: str):
    post = Post.objects(id=post_id).first()
    print(post)
    return post
 
def get_posts(skip: int = 0, limit: int = 10):
    posts = Post.objects()
    return [
        PostResponse(
            title=post.title,
            content=post.content,
            author=str(post.author.id),
            _id=str(post.id)
        ) for post in posts
    ]
   