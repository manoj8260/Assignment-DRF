import os
import csv
from pathlib import Path
from PIL import Image
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from celery import shared_task
from apps.recipes.models import RecipeRatings, Recipes
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)
User = get_user_model()

@shared_task(bind=True)
def resize_recipe_image(self, recipe_id, image_path):
    logger.info(f"Task called for recipe_id={recipe_id}, image_path={image_path}")  # this works
    """Reduce the size of recipe images upon upload by Sellers and log size reduction"""
    try:
        full_path = os.path.join(settings.MEDIA_ROOT, image_path)

        if not os.path.exists(full_path):
            logger.warning(f"Recipe {recipe_id}: Image file not found at {full_path}")
            return f"No image found for recipe {recipe_id}"

        original_size = os.path.getsize(full_path)

        with Image.open(full_path) as image:
            image.thumbnail((800, 600), Image.Resampling.LANCZOS)
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
            image.save(full_path, optimize=True, quality=85)

        new_size = os.path.getsize(full_path)

        logger.info(f"Recipe {recipe_id} image resized successfully.")
        logger.info(f"Original size: {original_size / 1024:.2f} KB")
        logger.info(f"New size: {new_size / 1024:.2f} KB")
        logger.info(f"Reduction: {((original_size - new_size) / original_size) * 100:.2f}%")

        return f"Image resized successfully for recipe {recipe_id}"

    except Exception as e:
        logger.error(f"Error resizing image for recipe {recipe_id}: {str(e)}")
        return f"Error resizing image: {str(e)}"


@shared_task
def send_daily_emails():
    """
    Send daily emails at 6 AM on weekdays.
    """
    try:
        users = User.objects.filter(is_active=True, is_staff=False)
        for user in users:
            send_mail(
                subject="Daily Update from Recipe Platform",
                message=f"Hello {user.first_name},\nHere’s your daily update!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email]
            )
            logger.info(f"Email sent to {user.email}")
        logger.info(f"All daily emails sent successfully. Total users: {users.count()}")
    except Exception as e:
        logger.error(f"Error sending daily emails: {str(e)}")

@shared_task(bind=True)
def backup_user_data(self):
    """
    Weekly scheduled service to backup user data locally.
    """
    try:
        backup_dir = Path(settings.BASE_DIR) / 'backups'
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = timezone.localtime().strftime('%Y%m%d_%H%M%S')

        # Backup Users
        users_file = backup_dir / f'users_{timestamp}.csv'
        with open(users_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'FirstName', 'Email', 'DateJoined'])
            for user in User.objects.all():
                writer.writerow([user.id, user.first_name, user.email, user.date_joined])
        logger.info(f"User data backup created at {users_file}")

        # Backup Recipes
        recipes_file = backup_dir / f'recipes_{timestamp}.csv'
        with open(recipes_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Name', 'CreatedBy', 'CreatedAt'])
            for recipe in Recipes.objects.select_related('created_by').all():
                writer.writerow([recipe.id, recipe.name, recipe.created_by.first_name, recipe.created_at])
        logger.info(f"Recipe data backup created at {recipes_file}")

        # Backup Ratings
        ratings_file = backup_dir / f'ratings_{timestamp}.csv'
        with open(ratings_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Recipe', 'User', 'Rating', 'CreatedAt'])
            for rating in RecipeRatings.objects.select_related('recipe', 'user').all():
                writer.writerow([rating.id, rating.recipe.name, rating.user.first_name, rating.rating, rating.created_at])
        logger.info(f"Ratings data backup created at {ratings_file}")

        return f"Backup completed successfully at {timestamp}"

    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        return f"Backup failed: {str(e)}"
