from django.contrib import admin

from .models import TournamentResult, BountyEvent


# Register your models here.
@admin.register(TournamentResult)
class TournamentResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournament', 'user')


@admin.register(BountyEvent)
class BountyEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'killer', 'killed')