from pydantic import BaseModel,Field
from typing import Optional,List
from bson import ObjectId
from datetime import datetime
 
class AuthorSchema(BaseModel):
    user_id: str
    bio: Optional[str] = None
 
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
 
class AuthorUpdateSchema(BaseModel):
    bio: Optional[str] = None
 
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
 
class UserSchema(BaseModel):
    id: Optional[str] = None
 
class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    username: str
    email: str
class AuthorResponse(BaseModel):
    user: UserSchema
    bio: Optional[str] = None
    id: Optional[str] = None
 
class CommentCreate(BaseModel):
    content: str
    author_id: str
 
class CommentUpdate(BaseModel):
    content: Optional[str] = None
 
class CommentResponse(BaseModel):
    id: str
    content: str
    author: str
    created_at: datetime
 
class PostCreate(BaseModel):
    title: str
    content: str
    author_id: str
 
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
 
class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    comments: List[CommentResponse] = []
    created_at: datetime
    updated_at: datetime
   