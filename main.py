from fastapi import FastAPI
from mongoengine import connect
from authenticator.auth import router as auth_router
from post.post import router as post_router

app = FastAPI()

# Connect to MongoDB
connect(host="mongodb://admin:password@localhost:27017/BLOGAPP?authSource=admin")

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(post_router, prefix="/post", tags=["post"])
