import os

from celery import Celery

from core.settings import REDIS_BASE_URL, TIME_ZONE, BASE_DIR, GETGEOAPI_UPDATE_INTERVAL, UZUM_BANK_UPDATE_INTERVAL

app = Celery('core')

app.config_from_object('core.settings', namespace='CELERY')

app.conf.result_backend = REDIS_BASE_URL + '/1'
app.conf.timezone = TIME_ZONE
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

# Celery beat schedule
app.conf.beat_schedule = {
    'retrieve_uzum_exchange_rates': {
        'task': 'converter.tasks.retrieve_uzum_exchange_rates',
        'schedule': 30
    },
}

module_names = []
modules = os.listdir(BASE_DIR)
for module in modules:
    if os.path.isdir(os.path.join(BASE_DIR, module)) and \
            os.path.exists(os.path.join(BASE_DIR, module, 'tasks.py')):
        module_names.append(f'{module}.tasks')

app.autodiscover_tasks(module_names, force=True)
