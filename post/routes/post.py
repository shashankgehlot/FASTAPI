from fastapi import APIRouter, HTTPException,Depends,status
from mongoengine import DoesNotExist
from post.models import Post, Author,Comment
from authenticator.models import User
from authenticator.schemas import User as UserSchema
from authenticator.utils import get_current_user,check_current_user_is_admin,is_admin,is_post_author
from post.schemas import CommentCreate, CommentUpdate, CommentResponse, PostCreate, PostUpdate, PostResponse
import json
from bson import ObjectId
from typing import List, Optional
 
router = APIRouter()
 
@router.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate, current_user: UserSchema = Depends(get_current_user)):
    author = Author.objects(id=post.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_post = Post(title=post.title, content=post.content, author=author)
    new_post.save()
    return PostResponse(
        id=str(new_post.id),
        title=new_post.title,
        content=new_post.content,
        comments=[],
        created_at=new_post.created_at,
        updated_at=new_post.updated_at
    )
 
@router.post("/posts/{post_id}/comments/", response_model=CommentResponse)
def add_comment(post_id: str, comment: CommentCreate, current_user: UserSchema = Depends(get_current_user)):
    post = Post.objects(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    author = User.objects(id=comment.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_comment = Comment(content=comment.content, author=author)
    post.comments.append(new_comment)
    post.save()
    return CommentResponse(
        id=str(new_comment.id),
        content=new_comment.content,
        author=new_comment.author.username,
        created_at=new_comment.created_at
    )
 
@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: str):
    post = Post.objects(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = [
        CommentResponse(
            id=str(comment.id),
            content=comment.content,
            author=comment.author.username,
            created_at=comment.created_at
        ) for comment in post.comments
    ]
    return PostResponse(
        id=str(post.id),
        title=post.title,
        content=post.content,
        comments=comments,
        created_at=post.created_at,
        updated_at=post.updated_at
    )
 
@router.get("/posts/", response_model=List[PostResponse])
def get_all_posts():
    posts = Post.objects()
    response = []
    for post in posts:
        comments = [
            CommentResponse(
                id=str(comment.id),
                content=comment.content,
                author=comment.author.username,
                created_at=comment.created_at
            ) for comment in post.comments
        ]
        response.append(
            PostResponse(
                id=str(post.id),
                title=post.title,
                content=post.content,
                comments=comments,
                created_at=post.created_at,
                updated_at=post.updated_at
            )
        )
    return response
 
def can_update_or_delete_post(post_id: str, current_user: User = Depends(get_current_user)):
    try:
        post = Post.objects.get(id=post_id)
        if current_user.is_admin or post.author.user == current_user:
            return post
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")
   
@router.delete("/posts/{post_id}")
async def delete_post(post: Post = Depends(can_update_or_delete_post)):
    post.delete()
    return {"message": "Post deleted successfully"}
 
@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_update: PostUpdate, post: Post = Depends(can_update_or_delete_post)):
    if post_update.title:
        post.title = post_update.title
    if post_update.content:
        post.content = post_update.content
    post.save()
    comments = [
        CommentResponse(
            id=str(comment.id),
            content=comment.content,
            author=comment.author.username,
            created_at=comment.created_at
        ) for comment in post.comments
    ]
    return PostResponse(
        id=str(post.id),
        title=post.title,
        content=post.content,
        comments=comments,
        created_at=post.created_at,
        updated_at=post.updated_at
    )
 
def can_modify_comment(post_id: str, comment_id: str, current_user: User = Depends(get_current_user)):
    try:
        post = Post.objects().get(id=post_id)
        comment = next((comment for comment in post.comments if str(comment.id) == comment_id), None)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        if current_user.is_admin or post.author == current_user or comment.author == current_user:
            return post, comment
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this comment")
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
 
@router.delete("/posts/{post_id}/comments/{comment_id}")
def delete_comment(post_comment: tuple = Depends(can_modify_comment)):
    post, comment = post_comment
    post.comments.remove(comment)
    post.save()
    return {"message": "Comment deleted successfully"}
 
@router.put("/posts/{post_id}/comments/{comment_id}", response_model=CommentResponse)
def update_comment(comment_update: CommentUpdate, post_comment: tuple = Depends(can_modify_comment)):
    post, comment = post_comment
    if comment_update.content:
        comment.content = comment_update.content
    post.save()
    return CommentResponse(
        id=str(comment.id),
        content=comment.content,
        author=comment.author.username,
        created_at=comment.created_at
    )