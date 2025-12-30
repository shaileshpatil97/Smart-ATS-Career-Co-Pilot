#!/bin/bash
celery -A ats_core worker -l info -P solo &
gunicorn ats_core.wsgi:application --bind 0.0.0.0:$PORT
