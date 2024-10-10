from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel
from typing import Optional
from authenticator.models import User
from authenticator.schemas import UserCreate, UserLogin, Token
from authenticator.schemas import User as UserSchema

from authenticator.utils import get_password_hash, verify_password, create_access_token,get_current_user

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    if User.objects(username=user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if User.objects(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_doc = User(username=user.username, email=user.email, password=hashed_password)
    user_doc.save()

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_doc = User.objects(username=form_data.username).first()
    if user_doc is None or not verify_password(form_data.password, user_doc.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me",response_model=UserSchema)
async def read_users_me(current_user:UserSchema = Depends(get_current_user)):
    return current_user