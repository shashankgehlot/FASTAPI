from fastapi import APIRouter, Depends, HTTPException, status
from mongoengine import DoesNotExist
from post.models import Author
from authenticator.models import User
from post.schemas import AuthorSchema,AuthorResponse, UserResponse, AuthorUpdateSchema
from authenticator.schemas import User as UserSchema
from authenticator.utils import check_current_user_is_admin , get_current_user
from bson import ObjectId
import json
router = APIRouter()
 
 
async def is_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return current_user
 
@router.post("/", response_model=AuthorResponse)
def create_author(author: AuthorSchema , current_user: UserSchema = Depends(is_admin_user)):
    user = User.objects.get(id=ObjectId(author.user_id))
    author_doc = Author(user=user, bio=author.bio)
    user.is_author = True
    user.save()
    author_doc.save()
    author_data = json.loads(author_doc.to_json())
    user_data = User.objects.get(id=ObjectId(author_data["user"]["$oid"]))
    user_data = json.loads(user_data.to_json())
    return {
        "user": {
            "id": user_data["_id"]["$oid"],
            "username": user_data["username"],
            "email": user_data["email"]
        },
        "bio": author_data["bio"],
        "id": author_data["_id"]["$oid"]
    }
 
@router.get("/{author_id}", response_model=AuthorResponse)
def read_author(author_id: str, current_user: UserSchema = Depends(get_current_user)):
    # try:
    author = Author.objects.get(id=ObjectId(author_id))
    author_data = json.loads(author.to_json())
    user_data = User.objects.get(id=ObjectId(author_data["user"]["$oid"]))
    user_data = json.loads(user_data.to_json())
    return {
        "user": {
            "id": user_data["_id"]["$oid"],
            "username": user_data["username"],
            "email": user_data["email"]
        },
        "bio": author_data["bio"],
        "id": author_data["_id"]["$oid"]
    }


@router.get("/user/{user_id}", response_model=AuthorResponse)
def read_author_by_userid(user_id: str, current_user: UserSchema = Depends(get_current_user)):
    author = Author.objects.get(user=ObjectId(user_id))
    author_data = json.loads(author.to_json())
    user_data = User.objects.get(id=ObjectId(author_data["user"]["$oid"]))
    user_data = json.loads(user_data.to_json())
    return {
        "user": {
            "id": user_data["_id"]["$oid"],
            "username": user_data["username"],
            "email": user_data["email"]
        },
        "bio": author_data["bio"],
        "id": author_data["_id"]["$oid"]
    }
 
@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: str, author: AuthorUpdateSchema, current_user: UserSchema = Depends(is_admin_user)):
    try:
        author_doc = Author.objects.get(id=ObjectId(author_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Author not found")
    author_doc.bio = author.bio
    author_doc.save()
    author_data = json.loads(author_doc.to_json())
    user_data = User.objects.get(id=ObjectId(author_data["user"]["$oid"]))
    user_data = json.loads(user_data.to_json())
    return {
        "user": {
            "id": user_data["_id"]["$oid"],
            "username": user_data["username"],
            "email": user_data["email"]
        },
        "bio": author_data["bio"],
        "id": author_data["_id"]["$oid"]
    }
 
 
@router.delete("/{author_id}")
def delete_author(author_id: str):
    try:
        author_doc = Author.objects.get(id=ObjectId(author_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Author not found")
    author_doc.delete()
    return {"detail": "Author deleted"}
 