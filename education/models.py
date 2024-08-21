from django.db import models
from config import settings


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название курса')
    preview = models.ImageField(
        upload_to='course/',
        blank=True,
        null=True,
        verbose_name='Изображение-превью'
    )
    description = models.TextField(
        verbose_name='Описание курса',
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='courses',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название урока')
    preview = models.ImageField(
        upload_to='course/',
        blank=True,
        null=True,
        verbose_name='Изображение-превью'
    )
    description = models.TextField(
        verbose_name='Описание урока',
        blank=True,
        null=True
    )
    video = models.URLField(
        verbose_name='Видео',
        blank=True,
        null=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='lessons',
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='lessons',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    expires_at = models.DateTimeField(
        verbose_name="Дата окончания подписки",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Статус подписки(активная/неактивная)",
    )
    period = models.PositiveIntegerField(
        default=30,
        verbose_name="Периодичность подписки",
    )