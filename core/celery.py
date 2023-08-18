import os

from celery import Celery

from core.settings import REDIS_BASE_URL, TIME_ZONE, BASE_DIR

app = Celery('core')

app.config_from_object('core.settings', namespace='CELERY')

app.conf.result_backend = REDIS_BASE_URL + '/1'
app.conf.timezone = TIME_ZONE
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

module_names = []
modules = os.listdir(BASE_DIR)
for module in modules:
    if os.path.isdir(os.path.join(BASE_DIR, module)) and \
            os.path.exists(os.path.join(BASE_DIR, module, 'tasks.py')):
        module_names.append(f'{module}.tasks')

app.autodiscover_tasks(module_names, force=True)
