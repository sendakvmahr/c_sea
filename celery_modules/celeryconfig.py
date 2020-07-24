
from celery import Celery
from celery.schedules import crontab

app = Celery('c_sea',
            backend='redis://localhost', 
            broker='pyamqp://'
#            include=['tasks'] #References your tasks. Donc forget to put the whole absolute path.
    )

app.conf.update(
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TIMEZONE = 'US/Pacific',
    CELERY_ENABLE_UTC = True
)   


