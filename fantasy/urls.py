from django.urls import path
from fantasy import views

app_name = 'fantasy'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('zawodnicy/', views.show_players, name='zawodnicy'),
    path('players/', views.get_players, name='players'),
]