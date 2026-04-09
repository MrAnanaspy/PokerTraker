from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from User.models import Users
from History.models import TournamentResult, BountyEvent
from Timer.models import Timer
from Game.models import Tournament
import json


def get_timer(request, id):
    tournament = Tournament.objects.get(id=id)
    results = TournamentResult.objects.filter(tournament=tournament)
    timer = Timer.objects.filter(tournament=tournament)

    return render(request, "timer.html")


def get_timer_data(request, id):
    tournament = Tournament.objects.get(id=id)
    results = TournamentResult.objects.filter(tournament=tournament)
    history = BountyEvent.objects.filter(killer__in=results)

    data = {
        "results": list(results.values(
            "id",
            "place",
            "join",
            "user__id",
            "user__username",
            "user__telegram_id",
            "user__score"
        )),
        "history": list(history.values(
            "id",
            "killer__user__username",
            "killed__user__username",
            "time"
        ))


    }
    print(data)

    return JsonResponse(data)


def knockout(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            tournament_id = data.get("tournament_id")
            knocker_id = data.get("knocker_id")
            target_id = data.get("target_id")

            if knocker_id:
                knocker = TournamentResult.objects.get(id=knocker_id)
            else:
                knocker = None

            target = TournamentResult.objects.get(id=target_id)
            count_players = TournamentResult.objects.filter(Q(tournament__id=tournament_id) & Q(place=None)).count()

            target.place = count_players
            target.save()

            BountyEvent.objects.create(killer=knocker, killed=target,)

            return JsonResponse({
                "status": "ok",
                "tournament_id": tournament_id
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)


def revive(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            tournament_id = data.get("tournament_id")
            player_result_id = data.get("player_result_id")

            player_result = TournamentResult.objects.get(id=player_result_id)

            player_result.place = None
            player_result.save()

            return JsonResponse({
                "status": "ok",
                "tournament_id": tournament_id
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)