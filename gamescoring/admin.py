from django.contrib import admin

from .models import GameNumber,Participant


class ParticipantInline(admin.TabularInline):
    model = Participant


class GameNumberAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]


admin.site.register(GameNumber, GameNumberAdmin)
admin.site.register(Participant)

