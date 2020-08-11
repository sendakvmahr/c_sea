from celery_modules.celeryconfig import app as app
from celery.decorators import task
from celery.task import Task
from text import input_document_spacy 
from communication import send_email
import datetime, os, random
import config


if config.computer_name in config.tiers["router"] :
	@task
	def send_daily_email():
		print("email sent")	


if config.computer_name in config.tiers["router"] or config.computer_name in config.tiers["tier_1"]:

	@task
	def process_files():
		print("a file has been processed.")	

	@task
	def read_file(read_until):
		stoptime = datetime.datetime.now().replace(hour=read_until) 
		processed_files = []
		files = os.listdir(os.path.abspath(config.to_read_dir))
		while datetime.datetime.now() < stoptime and len(files) != 0:
			read_dir = os.path.abspath(config.to_read_dir)
			files = os.listdir(read_dir)
			working_file = random.choice(files)
			working_file_dir = os.path.join(read_dir, working_file)
			input_document_spacy.read_data(working_file_dir)
			os.rename(working_file_dir, os.path.join(os.path.abspath(config.done_read_dir), working_file))
			processed_files.append(working_file)
		send_email.send_email("The following files were processed last night.\n{}\n\nThere are {} left to go.".format("\n".join(processed_files), len(files)))
