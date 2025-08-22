from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from apps.recipes.views import trigger_daily_emails, TriggerBackupView

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # Authentication module URLs (register, login, logout)
    path('api/auth/', include('apps.authentication.urls')),

    # Recipes module URLs (CRUD for recipes, ratings)
    path('api/recipes/', include('apps.recipes.urls')),

    # Trigger daily email Celery task(testing)
    path('emails/', trigger_daily_emails, name='trigger-daily-emails'),

    # Trigger backup Celery task (testing)
    path('backup/', TriggerBackupView.as_view(), name='trigger-backup'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
