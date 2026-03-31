from django.db import models
import django
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Achievements(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название достижения',
    )
    icon = models.ImageField(
        upload_to='icons/achievements/',
        blank=True,
        null=True,
        verbose_name='Иконка'
    )
    rare = models.FloatField(
        default=100,
        verbose_name='Редкость'
    )
    description = models.TextField(
        verbose_name='Описание достижения',
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'


class Users(AbstractUser):
    telegram_id = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name='id_tg'
    )
    #castom
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    score = models.FloatField(verbose_name='Рейтинг', default=1000,)

    achievements = models.ManyToManyField(
        Achievements,
        through='PlayerAchievements'
    )

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = 'Игрок в покер'
        verbose_name_plural = 'Игроки в покер'

class PlayerAchievements(models.Model):
    achievement = models.ForeignKey(
        Achievements,
        on_delete=models.CASCADE,
        verbose_name='Достижения'
    )
    player = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name='Игрои'
    )
    activ = models.BooleanField(
        default=False,
        verbose_name='Отоброжение'
    )
    date = models.DateField(verbose_name='Дата выдачи', default=django.utils.timezone.now)
    description = models.TextField(
        verbose_name='Описание кто и за что выдал',
    )

    def __str__(self):
        return f"{self.player} - {self.achievement}"

    class Meta:
        verbose_name = 'Достижение игрока'
        verbose_name_plural = 'Достижения игрока'

