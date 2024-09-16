from pydantic import BaseModel,EmailStr
from bson import ObjectId
 
   
class UserBase(BaseModel):
    username: str
    email: EmailStr
 
class UserCreate(UserBase):
    pass
 
class User(UserBase):
    id: str
 
    class Config:
        orm_mode = True
 
class UserResponseSchema(BaseModel):
    id: str
    email: str
    username: str
    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }
 
 
class AuthorBase(BaseModel):
    user_id: str
    bio: str
 
 
class AuthorCreate(AuthorBase):
    pass
 
    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }
       
class Author(BaseModel):
    id: str
    user_id: str
    bio: str
 
    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }
 
class PostBase(BaseModel):
    title: str
    content: str
    author_id: str
 
class PostCreate(PostBase):
    pass
 
class Post(BaseModel):
    title: str
    content: str
    author: str
    _id: str
 
    class Config:
        orm_mode = True    
 
 
class PostResponse(BaseModel):
    title: str
    content: str
    author: str
    _id: str
 
    class Config:
        orm_mode = True