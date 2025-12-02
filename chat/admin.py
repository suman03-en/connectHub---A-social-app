from django.contrib import admin
from .models import Room,ChatMessage
# Register your models here.

class RoomAdmin(admin.ModelAdmin):

    list_display = ('name', 'display_participants')
    
    def display_participants(self, obj):

        return ", ".join([user.username for user in obj.participants.all()])

    display_participants.short_description = 'Participants'

admin.site.register(Room, RoomAdmin)
admin.site.register(ChatMessage)