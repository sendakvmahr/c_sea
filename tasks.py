from celeryconfig import app
@app.task
def add(x, y):
	return x + y

print("it ran")

# celery -A cluster worker --loglevel=info