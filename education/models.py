from django.db import models


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
    video = models.FileField(
        upload_to='course/',
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

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.name

