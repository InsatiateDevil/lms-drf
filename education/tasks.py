from celery import shared_task
from django.core.mail import send_mail

from config import settings
from education.models import Course, Subscription


@shared_task
def subscribers_notification(course_id):
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course)
    for subscription in subscriptions:
        send_mail(
            subject=f'Обновление курса {course.name}',
            message=f'Уведомляем вас о обновлении курса {course.name}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email,],
        )

