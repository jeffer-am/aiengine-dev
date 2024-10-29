# apps/aiengine/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define as configurações do Django para o Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("aiengine")

# Lê configurações do Django e prefixa com `CELERY_`
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-descobre tarefas registradas nas apps do Django
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
