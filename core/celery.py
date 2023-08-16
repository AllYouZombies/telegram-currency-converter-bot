from celery import Celery

from core.settings import REDIS_BASE_URL, TIME_ZONE

app = Celery('core')

app.config_from_object('core.settings', namespace='CELERY')

app.conf.result_backend = REDIS_BASE_URL + '/1'
app.conf.timezone = TIME_ZONE
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

app.autodiscover_tasks()
