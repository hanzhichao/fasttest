APP=fasttest
FLOWER_PORT=7777

cd ..
celery -A ${APP} flower --port=${FLOWER_PORT}
