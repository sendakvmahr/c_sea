from celery import Celery
from celery.schedules import crontab
from celery_modules.celeryconfig import app as app
import celery_modules.tasks as tasks
import config

app.conf.update(
    CELERY_DEFAULT_QUEUE = "processor",
    CELERY_ROUTES = {
		"celery_modules.tasks.process_files" : {"queue" : "processor"},
		"celery_modules.tasks.send_daily_email" : {"queue" : "router"},
		"celery_modules.tasks.assign_nightly_processing" : {"queue" : "router"},
	}
)   

app.conf.CELERYBEAT_SCHEDULE = {
    'every-5-seconds': {
        'task': 'celery_modules.tasks.process_files',
        'schedule': 20.0,
        'options': {'queue': 'router'},
    },
    'daily_email': {
        'task': 'celery_modules.tasks.send_daily_email',
        'schedule': crontab(hour=23, minute=53),
        'options': {'queue': 'router'},
    },
}

# app.control.broadcast('shutdown') # shutdown all workers