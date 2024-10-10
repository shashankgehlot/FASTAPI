from celery_app import celery_app
 
 
@celery_app.task
def my_task(x, y):
   ans = x + y
   print(ans)
   return ans