import os
from celery import Celery
from ssl import CERT_NONE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StudyMate.settings")
app = Celery(
    "StudyMate",
    broker_use_ssl={"ssl_cert_reqs": CERT_NONE},
    redis_backend_use_ssl={"ssl_cert_reqs": CERT_NONE},
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
