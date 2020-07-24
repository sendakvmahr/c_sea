#!/usr/bin/env bash
source env/bin/activate
celery -A celery_modules.periodic_reading worker --loglevel=info 