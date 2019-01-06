# celery -A cluster worker --loglevel=info

from tasks import add
result = add.delay(4, 4)
result.ready()
