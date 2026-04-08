from django.db import models

from Game.models import Tournament


# Create your models here.
class Timer(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        verbose_name='Игра'
    )
    end_time = models.DateTimeField(null=True, blank=True)
    remaining_seconds = models.IntegerField(
        default=0,
        verbose_name='Время от старта, сек'
    )
    is_paused = models.FloatField(
        default=True,
        verbose_name='Статус таймера'
    )


    class Meta:
        unique_together = ['tournament']
        verbose_name = 'Таймер'
        verbose_name_plural = 'Таймеры'