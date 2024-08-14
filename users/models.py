from django.contrib.auth.models import AbstractUser
from django.db import models

from education.models import Course, Lesson


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='email',
        help_text='Введите ваш email'
    )
    phone_number = models.CharField(
        max_length=25,
        verbose_name='телефон',
        help_text='Введите ваш номер телефона',
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name='аватар',
        help_text='Выберите аватар',
        blank=True,
        null=True
    )
    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Город',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма платежа')
    method = models.CharField(max_length=100, verbose_name='Способ оплаты')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        if self.lesson:
            return f'{self.user} - {self.lesson}'
        else:
            return f'{self.user} - {self.course}'

