from django.db import models
import django
from django.utils import timezone

from Game.models import Tournament
from User.models import Users


# Create your models here.
class TournamentResult(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        verbose_name='Турнир'
    )
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name='Игрок'
    )
    place = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Место'
    )
    rating_before = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Рейтинг ДО'
    )
    rating_change = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Получиный рейтинг'
    )
    inputs = models.IntegerField(
        default= 1,
        verbose_name='Количество докупов'
    )
    place_at_the_table = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Место за столом'
    )
    join = models.DateTimeField(
        default=timezone.now,
        verbose_name='Время регистрации'
    )

    class Meta:
        unique_together = ['user', 'tournament']
        verbose_name = 'История турнира'
        verbose_name_plural = 'История турниров'


class BountyEvent(models.Model):
    killer = models.ForeignKey(
        TournamentResult,
        on_delete=models.CASCADE,
        verbose_name='Результат турнира',
        related_name='killer'
    )
    killed = models.ForeignKey(
        TournamentResult,
        on_delete=models.CASCADE,
        verbose_name='Кого выбил',
        related_name='killed'
    )
    bounty = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Сколько получил за выбивание'
    )
    time = models.DurationField(
        null=True,
        blank=True,
        verbose_name='Время от начала игры'
    )

    class Meta:
        verbose_name = 'Выбивание'
        verbose_name_plural = 'Выбивания'