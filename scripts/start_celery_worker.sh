APP=fasttest
LOGLEVEL=INFO
CONCURRENCY=10

cd ..
celery -A ${APP} worker -l ${LOGLEVEL} --concurrency=${CONCURRENCY} -n worker1.%h
