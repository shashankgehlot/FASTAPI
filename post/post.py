from fastapi import APIRouter, HTTPException, Depends, status
from post import schemas, utils
 
from typing import List
 
router = APIRouter()
 
 
@router.get("/users/{user_id}", response_model=schemas.UserResponseSchema)
def read_user(user_id: str):
    db_user = utils.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
 
@router.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(author: schemas.AuthorCreate):
    db_author = utils.create_author(author)
    if db_author is None:
        raise HTTPException(status_code=400, detail="User not found")
    return schemas.AuthorCreate(user_id=str(db_author.user_id.id), bio=db_author.bio)
 
@router.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: str):
    db_author = utils.get_author(author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return schemas.Author(id=str(db_author.id),user_id=str(db_author.user_id.id), bio= db_author.bio)
 
 
@router.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate):
    db_post = utils.create_post(post)
    if db_post is None:
        raise HTTPException(status_code=400, detail="Author not found")
    return schemas.Post(
        id=str(db_post.id),
        title=db_post.title,
        content=db_post.content,
        author_id=str(db_post.author.id)
    )
 
@router.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: str):
    db_post = utils.get_post(post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
 
@router.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 10):
    db_posts = utils.get_posts(skip=skip, limit=limit)
    return db_posts
