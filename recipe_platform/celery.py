import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_platform.settings')

app = Celery('recipe_platform')


app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks(["apps.recipes"])

# Hardcoded periodic tasks (Celery Beat)
app.conf.beat_schedule = {
    'daily-emails': {
        'task': 'apps.recipes.tasks.send_daily_emails',
        'schedule': crontab(hour=6, minute=0,day_of_week='1-5'), 
         'args': (),
    },
    'weekly-backup': {
        'task': 'apps.recipes.tasks.backup_user_data_locally',
        'schedule': crontab(hour=2, minute=0, day_of_week=1),  
    },
}


app.conf.update(
    task_serializer='json',
    accept_content=['json'],  
    result_serializer='json',
    timezone=settings.TIME_ZONE,
)
