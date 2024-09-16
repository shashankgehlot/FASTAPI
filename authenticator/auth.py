from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
from authenticator.models import User
from authenticator.schemas import UserCreate, UserLogin, Token
from authenticator.utils import get_password_hash, verify_password, create_access_token

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
async def login(user: UserLogin):
    user_doc = User.objects(username=user.username).first()
    if user_doc is None or not verify_password(user.password, user_doc.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout():
    # In this simple example, we're not handling token invalidation
    return {"msg": "Logged out successfully"}
