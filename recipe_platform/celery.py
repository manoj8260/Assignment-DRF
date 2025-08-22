import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_platform.settings')

app = Celery('recipe_platform')

# Load configuration from Django settings, the CELERY namespace means all celery-related config keys
# should be prefixed with "CELERY_"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks(["apps.recipes"])

# Hardcoded periodic tasks (Celery Beat)
app.conf.beat_schedule = {
    'daily-emails': {
        'task': 'apps.recipes.tasks.send_daily_emails',
        'schedule': crontab(hour=14, minute=17,day_of_week='1-5'), 
         'args': (),
    },
    'weekly-backup': {
        'task': 'apps.recipes.tasks.backup_user_data_locally',
        'schedule': crontab(hour=2, minute=0, day_of_week=1),  # Every Monday at 2 AM
    },
}
print(settings.TIME_ZONE)
# General Celery settings
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone=settings.TIME_ZONE,
)
