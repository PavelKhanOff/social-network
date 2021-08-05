from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email', max_length=255, unique=True)
    last_activity = models.DateTimeField(
        default=None, blank=True,
        null=True, verbose_name='Last Made Request')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
