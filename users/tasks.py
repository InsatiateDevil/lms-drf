from datetime import timedelta, datetime
from pytz import timezone
from celery import shared_task

from config import settings
from users.models import User


@shared_task
def check_last_login_and_disactivate_user():
    users = User.objects.filter(is_active=True)
    time_zone = timezone(settings.TIME_ZONE)
    current_date = datetime.now(time_zone)
    for user in users:
        if user.last_login and user.last_login + timedelta(days=30) < current_date:
            user.is_active = False
            user.save()

