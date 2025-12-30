#!/bin/bash
celery -A ats_core worker -l info &
gunicorn ats_core.wsgi
