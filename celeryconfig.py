from celery import Celery

app = Celery('celeryconfig',
             broker='amqp://guest@localhost//',
             backend='amqp://guest@localhost//',
             include=['tasks'] #References your tasks. Donc forget to put the whole absolute path.
             )

app.conf.update(
        CELERY_TASK_SERIALIZER = 'json',
        CELERY_RESULT_SERIALIZER = 'json',
        CELERY_ACCEPT_CONTENT=['json'],
        CELERY_TIMEZONE = 'Europe/Oslo',
        CELERY_ENABLE_UTC = True
                )