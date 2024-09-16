from fastapi import FastAPI
from mongoengine import connect
from authenticator.auth import router as auth_router

app = FastAPI()

# Connect to MongoDB
connect(host="mongodb://admin:password@88.222.241.12:27017/BLOGAPP?authSource=admin")

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])