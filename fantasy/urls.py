from django.urls import path
from fantasy import views

app_name = "fantasy"

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("restricted/", views.restricted, name="restricted"),
    path("logout/", views.user_logout, name="logout"),
    path("players/", views.PlayerList.as_view(), name="players"),
    path("players/<int:pk>", views.PlayerDetail.as_view()),
    path("clubs", views.ClubList.as_view(), name="clubs-list"),
    path("fantasy-clubs", views.FantasyClubList.as_view(), name="fantasy-clubs-list"),
    path("testing", views.create_fantasy_club, name="create-fantasy-club"),
]
