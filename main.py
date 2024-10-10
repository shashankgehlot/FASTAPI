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
from celery_app import my_task
import uvicorn
import os
app = FastAPI()
 
USERNAME = "admin"
PASSWORD = "secret"
security = HTTPBasic()
# Connect to MongoDB
username=os.getenv("MONGO_INITDB_ROOT_USERNAME")
password=os.getenv('MONGO_INITDB_ROOT_PASSWORD')
connect(host="mongodb://{username}:{password}@88.222.213.152:27017/TESTDATA?authSource=admin")
 
 
# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(author_router, prefix="/author", tags=["author"])
app.include_router(post_router, prefix="/blog", tags=["post"])
 
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

def start_celery_worker():
    subprocess.run(["celery", "-A", "celery_app.celery_app", "worker", "--loglevel=info"])
 
def start_flower():
    subprocess.run(["celery", "-A", "celery_app.celery_app", "flower","--port=5555"])
 
@app.on_event("startup")
def start_background_services():
    # Start Celery worker in a separate thread
    threading.Thread(target=start_celery_worker).start()
   
    # Start Flower in a separate thread
    threading.Thread(target=start_flower).start()