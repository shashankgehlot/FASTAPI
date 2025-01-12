from fastapi import FastAPI, Depends, HTTPException, Security,BackgroundTasks
from fastapi import FastAPI, BackgroundTasks
import subprocess
import sys
import threading
from mongoengine import connect
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from authenticator.auth import router as auth_router
from post.routes.post import router as post_router
from post.routes.author import router as author_router
from tracker.routes.tracker import router as tracking_router
from celery_app import my_task
import uvicorn
import os

from dotenv import load_dotenv
load_dotenv()

USERNAME = "admin"
PASSWORD = "secret"
security = HTTPBasic()
app = FastAPI(root_path='/api')
# Connect to MongoDB
username=os.getenv("MONGO_INITDB_ROOT_USERNAME")
password=os.getenv('MONGO_INITDB_ROOT_PASSWORD')
url = f"mongodb://{username}:{password}@mongo:27017/TESTDATA?authSource=admin"
print(url)
connect(host=url)
 
 
# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(author_router, prefix="/author", tags=["author"])
app.include_router(post_router, prefix="/blog", tags=["post"])
app.include_router(tracking_router, prefix="/track", tags=["tracker"])

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == USERNAME and credentials.password == PASSWORD:
        return True
    raise HTTPException(status_code=401, detail="Invalid credentials")
 
@app.get("/secure-docs", dependencies=[Depends(verify_credentials)])
async def get_swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Secure Docs")
 
@app.get("/run")
def handle_run():
   task_response = my_task.delay(5, 6)
   return {"message": "Task execution started"}
