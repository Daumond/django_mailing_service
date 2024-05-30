from django.contrib.auth.models import AbstractUser
from django.db import models

from mailings.models import NULLABLE


# Create your models here.
class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    is_email_active = models.BooleanField(default=False, verbose_name='верификация по почте')
    is_active = models.BooleanField(default=True, verbose_name='признак активности')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        permissions = [
            (
                'view_all_clients',
                'can view all clients',
            ),
            (
                'set_active',
                'can activate clients',
            ),
        ]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []