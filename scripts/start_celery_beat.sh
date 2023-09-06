APP=fasttest
LOGLEVEL=INFO

cd ..
celery -A ${APP} beat -l ${LOGLEVEL} --scheduler django_celery_beat.schedulers:DatabaseScheduler


