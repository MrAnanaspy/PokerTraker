from django.contrib import admin

from .models import Tournament, Season


# Register your models here.
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'season')


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_start', 'date_end')
