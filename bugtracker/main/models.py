from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import UserManager


class Tasks(models.Model):
    tittle = models.CharField('Заголовок', max_length=75, unique=True)
    type = models.CharField('Тип', max_length=5)
    priority = models.CharField('Приоритет', max_length=15)
    text = models.TextField('Описание')
    status = models.CharField('Статус', max_length=40)
    datetime_create = models.DateTimeField('Дата создания', auto_now_add=True)
    datetime_update = models.DateTimeField('Дата изменения', auto_now=True)
    creator = models.ForeignKey('Users', on_delete=models.CASCADE)
    executor = models.CharField('Исполнитель', max_length=60, default=None)

    def __str__(self):
        return self.tittle


class Users(AbstractBaseUser):
    role = models.CharField('Роль', max_length=40, default='Разработчик')
    username = models.CharField('Имя пользователя', max_length=40, unique=True)
    password = models.CharField('Пароль', max_length=30)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
