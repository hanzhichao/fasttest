APP=fasttest
LOGLEVEL=INFO
CONCURRENCY=10

cd ..
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES celery -A ${APP} worker -l ${LOGLEVEL} --concurrency=${CONCURRENCY} -n worker1.%h
