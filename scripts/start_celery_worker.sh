cd .. && OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES  celery -A fasttest worker -l INFO --concurrency=10 -n worker1.%h && cd -
