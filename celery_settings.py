import os

CELERY_TASK_SERIALIZER = 'json'
CELERY_BROKER_URL = os.environ['CLOUDAMQP_URL']
# CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL','pyamqp://guest@localhost//')
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.db'
# CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL','redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
CELERY_ACCEPT_CONTENT = ['json']
