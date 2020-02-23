import os

CELERY_TASK_SERIALIZER = 'json'
CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL','pyamqp://guest@localhost//')
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.db'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
