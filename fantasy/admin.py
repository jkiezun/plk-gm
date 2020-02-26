from django.urls import path
from django.shortcuts import render
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.contrib import admin
from .models import ClubMember, Game, Club, FantasyClub, Player, PlayerStat, UserProfile


# Register your models here.
class Player_StatAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in PlayerStat._meta.fields if field.name != "id"]


class PlayerStatInline(admin.TabularInline):
    model = PlayerStat


class FantasyClubMemberInLine(admin.TabularInline):
    model = ClubMember
    extra = 2


class Player_Admin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'Club')
    inlines = (FantasyClubMemberInLine, PlayerStatInline)


class FantasyClubAdmin(admin.ModelAdmin):
    inlines = (FantasyClubMemberInLine,)


admin.site.register(Club)
admin.site.register(Player, Player_Admin)
admin.site.register(PlayerStat, Player_StatAdmin)
admin.site.register(Game)
admin.site.register(FantasyClub, FantasyClubAdmin)
