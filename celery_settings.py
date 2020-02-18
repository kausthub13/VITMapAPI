import os

CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL','pyamqp://guest@localhost//')
CELERY_RESULT_BACKEND = 'db+sqlite:///results.db'
