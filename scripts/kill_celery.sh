ps -ef | grep celery | awk '{print $2}' | xargs kill -9
