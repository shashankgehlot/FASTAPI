from fastapi import APIRouter, HTTPException,Depends,status,Query
from mongoengine import DoesNotExist,NotUniqueError
from post.models import Post, Author,Comment,Tags
from authenticator.models import User
from authenticator.schemas import User as UserSchema
from authenticator.utils import get_current_user,check_current_user_is_admin,is_admin,is_post_author
from post.schemas import CommentCreate, CommentUpdate, CommentResponse, PostCreate, PostUpdate, PostResponse,TagCreate
import json
from bson import ObjectId
from typing import List, Optional
 
router = APIRouter()
 
@router.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate, current_user: UserSchema = Depends(get_current_user)):
    if not current_user.is_author:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create a post")
    author = Author.objects(id=post.author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    try:
        new_post = Post(title=post.title, content=post.content, author=author)
        new_post.save()
        if post.tags:
            for tags in post.tags:
                new_post.add_tags(tags.title)
    except NotUniqueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title must be unique")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)
    return PostResponse(
        id=str(new_post.id),
        title=new_post.title,
        content=new_post.content,
        tags=[tag.title for tag in new_post.tags],
        created_at=new_post.created_at,
        updated_at=new_post.updated_at,
        slug_title=new_post.slug_title
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

@router.post("/posts/{post_id}/tags/add", response_model=None)
def add_tag(post_id: str, tags: List[TagCreate], current_user: UserSchema = Depends(get_current_user)):
    post = Post.objects(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for tag_data in tags:
        post.add_tags(tag_data.title)
    return {"message": "added tags successfully"}
 
@router.post("/posts/{post_id}/tags/remove", response_model=None)
def remove_tags(post_id: str, tags: List[TagCreate], current_user: UserSchema = Depends(get_current_user)):
    post = Post.objects(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for tag_data in tags:
        post.remove_tags(tag_data.title)
    return {"message": "removed tags successfully"}

@router.get("/tags/", response_model=List[TagCreate])
def get_all_tags():
    tags = Tags.objects()
    return [TagCreate(title=tag.title) for tag in tags]
 
@router.get("/posts/id/{post_id}", response_model=PostResponse)
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
    tags = [tag.title for tag in post.tags]
    return PostResponse(
        id=str(post.id),
        title=post.title,
        content=post.content,
        comments=comments,
        tags=tags,
        created_at=post.created_at,
        updated_at=post.updated_at,
        slug_title=post.slug_title,
    )
 
@router.get("/posts/slug/{slug_title}", response_model=PostResponse)
def get_post_by_slug(slug_title: str):
    post = Post.objects(slug_title=slug_title).first()
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
    tags = [tag.title for tag in post.tags]
    return PostResponse(
        id=str(post.id),
        title=post.title,
        content=post.content,
        tags=tags,
        comments=comments,
        created_at=post.created_at,
        updated_at=post.updated_at,
        slug_title=post.slug_title,
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
        tags = [tag.title for tag in post.tags]
        response.append(
            PostResponse(
                id=str(post.id),
                title=post.title,
                content=post.content,
                comments=comments,
                tags=tags,
                created_at=post.created_at,
                updated_at=post.updated_at,
                slug_title=post.slug_title
            )
        )
    return response

@router.get("/tagged-posts/", response_model=List[PostResponse])
def get_tagged_posts(tags: Optional[List[str]] = Query(None)):
    print(tags)
    if tags:
        tag_objects = Tags.objects(title__in=tags)
        tag_ids = [tag.id for tag in tag_objects]
        # Filtering posts by tag IDs
        posts = Post.objects(tags__in=tag_ids)
    else:
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
        tags = [tag.title for tag in post.tags]
        response.append(
            PostResponse(
                id=str(post.id),
                title=post.title,
                content=post.content,
                comments=comments,
                tags=tags,
                created_at=post.created_at,
                updated_at=post.updated_at,
                slug_title=post.slug_title
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
    #first remove all the tags
    if post.tags:
        for tag in post.tags:
            print("remove",tag.title)
            post.remove_tags(tag.title)
    #then add the updated new tags
    if post_update.tags:
        for tag_data in post_update.tags:
            print("add",tag_data.title)
            post.add_tags(tag_data.title)
    
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
        updated_at=post.updated_at,
        slug_title=post.slug_title,
        tags=[tag.title for tag in post.tags]
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
