import logging
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram.settings")
app = Celery("instagram")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.log.setup(loglevel='DEBUG')

logger = logging.getLogger('celery')

@app.task()
def ping():
    print('POOONG')


#email
# SERVER_EMAIL=localhost
# DJANGO_EMAIL_BACKEND=anymail.backends.mandrill.EmailBackend
# DJANGO_EMAIL_HOST=smtp.gmail.com
# DJANGO_EMAIL_PORT=587
#
# DJANGO_EMAIL_HOST_USER=yerenagmt2@gmail.com
# DJANGO_EMAIL_HOST_PASSWORD=shatavubiblstokg
#
# DEFAULT_FROM_EMAIL=noreply@omnibnk.com

