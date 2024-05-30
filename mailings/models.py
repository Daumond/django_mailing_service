from datetime import datetime

from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Client(models.Model):
    email = models.EmailField(verbose_name='электронная почта')
    surname = models.CharField(max_length=20, verbose_name='фамилия')
    name = models.CharField(max_length=20, verbose_name='имя')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'Клиент: {self.email}.'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    mail_subject = models.TextField(max_length=100, verbose_name='тема письма')
    mail_text = models.TextField(verbose_name='тело письма')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'Сообщение: {self.mail_subject}.'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )

    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    )

    name = models.CharField(max_length=100, verbose_name='название рассылки', default='Новая рассылка')
    mailing_time = models.DateTimeField(verbose_name='время рассылки')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name='периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)
    clients = models.ManyToManyField(Client, related_name='mailings', verbose_name='клиенты')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    is_active = models.BooleanField(default=True, verbose_name='признак активности')

    def __str__(self):
        return f'Рассылка {self.name}.'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    STATUS_CHOICES = (
        ('success', 'Успешно'),
        ('failed', 'Не удалось'),
    )

    timestamp = models.DateTimeField(default=datetime.now, verbose_name='дата и время попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    client = models.ManyToManyField(Client, related_name='logs', verbose_name='клиент')
    mailing_list = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='logs',
                                     verbose_name='рассылка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'Лог: "{self.mailing_list}"'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'