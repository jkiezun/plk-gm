from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from fantasy.forms import UserForm
from fantasy.models import Player, PlayerStat, Club, FantasyClub
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .add_stats import add_stats_by_game_id
from bs4 import BeautifulSoup
import requests
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from fantasy.serializers import PlayerSerializer, ClubSerializer, FantasyClubSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

# Create your views here.


def index(request):
    real_clubs = Club.objects.exclude(name="1liga")
    return render(request, "fantasy/index.html", {"real_clubs": real_clubs})


def register(request):
    registered = False

    if request.method == "POST":
        data = request.POST.copy()
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(
        request,
        "fantasy/register.html",
        {"user_form": user_form, "registered": registered},
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("fantasy:index"))
            else:
                return HttpResponse("Your PLKGM account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "fantasy/login.html")


@login_required
def restricted(request):
    return HttpResponse("since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("fantasy:index"))


class FantasyClubList(generics.ListCreateAPIView):
    queryset = FantasyClub.objects.all()
    serializer_class = FantasyClubSerializer


class ClubList(generics.ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    http_method_names = ["get"]


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


def update_stats_view(request):
    if request.user.is_superuser:
        if request.method == "POST":
            res = requests.get("https://www.plk.pl/")
            plk_page = res.text
            soup = BeautifulSoup(plk_page)
            played_games = soup.findAll("div", {"data-koniec": "1"})
            success = 1
            for game in played_games:
                game_id = game["data-game"]
                success = add_stats_by_game_id(game_id)
            if success:
                return render(
                    request, "admin/fantasy/addstats.html", {"result": "Success!"}
                )
            else:
                return render(
                    request, "admin/fantasy/addstats.html", {"result": "Some error"}
                )
        elif request.method == "GET":
            return redirect("/admin/fantasy")

    else:
        return redirect("/admin/fantasy")


def add_stats_view(request):
    if request.user.is_superuser:
        if request.method == "POST":
            game_id = request.POST["match_id"]
            success = add_stats_by_game_id(game_id)
            return render(request, "admin/fantasy/addstats.html", {"result": success})
        elif request.method == "GET":
            return redirect("/admin/fantasy")
    else:
        return redirect("/admin/fantasy")


def get_players(request):
    if request.method == "GET":
        data = serializers.serialize("json", Player.objects.all())
        return JsonResponse(data, safe=False)
    else:
        return redirect("/index")


@csrf_exempt
def create_fantasy_club(request):
    if request.method == "GET":
        return redirect("/")
    elif request.method == "POST":
        data = request.body
        print(data)
