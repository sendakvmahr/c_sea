from celery import Celery

app = Celery('c_sea',
            backend='redis://localhost', 
            broker='pyamqp://',
            include=['celery_modules.tasks'] 
    )

app.conf.update(
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TIMEZONE = 'US/Pacific',
    CELERY_ENABLE_UTC = True,
    CELERY_CREATE_MISSING_QUEUES = True
)   


