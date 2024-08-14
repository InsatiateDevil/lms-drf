from django.contrib.auth.models import AbstractUser
from django.db import models

from education.models import Course


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
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']
        permissions = (
            ('users.can_change_status', 'Может изменять статус пользователя'),
            (
            'users.can_view_users', 'Может просматривать список пользователей'),
        )

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=100)
