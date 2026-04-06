from django.db import models
import django


# Create your models here.
class Season(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        verbose_name='Название сезона'
    )
    description = models.TextField(
        verbose_name='Описание сезона',
    )
    date_start = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата начала'
    )
    date_end = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата завершения'
    )
    status = models.CharField(
        max_length=50,
        verbose_name='Статус сезона'
    )
    settings = models.JSONField(
        verbose_name='Настройки таймера на игры',
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'


class Tournament(models.Model):
    date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата'
    )
    season = models.ForeignKey(
        Season,
        on_delete=models.SET_NULL,
        verbose_name='Сезон',
        null=True
    )
    stack = models.IntegerField(
        default=1000,
        verbose_name='Стартовый стек'
    )
    cost = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Стоимость рейтинга'
    )
    settings = models.JSONField(
        verbose_name='Настройки таймера на игры',
    )
    time = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Время турнира'
    )
    ratio_BB = models.FloatField(
        default=0.5,
        verbose_name='Коэффициент ББ'
    )
    bounty = models.FloatField(
        default=0.5,
        verbose_name='Коэффициент баунти'
    )
    percentage_prize = models.FloatField(
        default=0.25,
        verbose_name='Процент призов'
    )
    percentage_rebay = models.FloatField(
        default=0.25,
        verbose_name='Процент роста ребая'
    )
    time_end_rebay = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Время закрытия ребаев'
    )

    def __str__(self):
        if self.date:
            return f"{self.id} - {self.date}"
        else:
            return f"{self.id} - дата не выбрана"

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'