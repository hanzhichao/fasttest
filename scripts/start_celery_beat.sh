cd .. && OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES celery -A fasttest beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler && cd - || exit


