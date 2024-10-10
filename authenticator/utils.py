from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
# import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from authenticator.models import User as UserModel
from authenticator.schemas import TokenData, User as UserSchema
from post.models import Post,Comment
from functools import wraps
 
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
 
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
 
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception:
        raise credentials_exception
 
    user = UserModel.objects(username=token_data.username).first()
    if user is None:
        raise credentials_exception
    print(UserSchema.from_orm(user))
    return user
 
 
 
async def check_current_user_is_admin(token: str = Depends(oauth2_scheme)) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception:
        raise credentials_exception
 
    user = UserModel.objects(username=token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
 
 
def get_post(post_id: str):
    post = Post.objects(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
 
def get_comment(post: Post, comment_id: str):
    comment = next((comment for comment in post.comments if str(comment.id) == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment
 
def is_admin(user: UserSchema) -> bool:
    print(">>>>>")
    print(user)
    return user.is_admin
 
def is_post_author(user: UserSchema, post: Post) -> bool:
    return str(post.author.user.id) == str(user.id)
 
def is_comment_author(user: UserSchema, comment: Comment) -> bool:
    return str(comment.author.id) == str(user.id)