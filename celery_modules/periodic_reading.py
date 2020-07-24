from celery import Celery
from celery.schedules import crontab
from celery_modules.celeryconfig import app as app
from text import input_document_spacy as inp
import time
import datetime
import os
import random
import config
from communication import send_email

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	#start reading files at midnight
	for i in range(3): # 3 computers planned
	    sender.add_periodic_task( 
	        crontab(hour=0, minute=0),
	        read_file.s(7),
	    )
	    sender.add_periodic_task( 
	        crontab(hour=9, minute=35),
	        read_file.s(16),
	    )

@app.task
def read_file(read_until):
	stoptime = datetime.datetime.now().replace(hour=read_until) 
	processed_files = []
	files = os.listdir(os.path.abspath(config.to_read_dir))
	while datetime.datetime.now() < stoptime and len(files) != 0:
		read_dir = os.path.abspath(config.to_read_dir)
		files = os.listdir(read_dir)
		working_file = random.choice(files)
		working_file_dir = os.path.join(read_dir, working_file)
		inp.read_data(working_file_dir)
		os.rename(working_file_dir, os.path.join(os.path.abspath(config.done_read_dir), working_file))
		processed_files.append(working_file)
	send_email.send_email("The following files were processed last night.\n{}\n\nThere are {} left to go.".format("\n".join(processed_files), len(files)))