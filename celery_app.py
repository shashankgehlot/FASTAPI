import os
from celery import Celery
import asyncio


BROKER_TRANSPORT = 'amqp'
BROKER_USERNAME = os.getenv("RABBITMQ_DEFAULT_USER")
BROKER_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")
BROKER_HOST =  os.getenv("HOST")
BROKER_PORT = '5672'

CELERY_BROKER_URL = "{}://{}:{}@{}:{}".format(
    BROKER_TRANSPORT, BROKER_USERNAME, BROKER_PASSWORD, BROKER_HOST, BROKER_PORT
)
print(CELERY_BROKER_URL)
BROKER_URL = CELERY_BROKER_URL
CELERY_RESULT_BACKEND ="rpc://"
 
 
celery_app = Celery(__name__, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
 
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_track_started=True
)
 
@celery_app.task
def my_task(x, y):
   ans = x + y
   print(ans)
   return ans
 
#celery_task.py
