from django.contrib import admin

from .models import TournamentResult


# Register your models here.
@admin.register(TournamentResult)
class TournamentResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournament', 'user')