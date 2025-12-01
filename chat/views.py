from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from chat.decorators import room_owner_required
from .models import Room

def index(request):
    return render(
        request,
        'chat/index.html'
    )

@room_owner_required
@login_required(login_url='login')
def room(request,room_name):

    obj, created = Room.objects.get_or_create(name=room_name)
    obj.participants.add(request.user)

    latest_messages = obj.messages.all()
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "latest_messages": latest_messages
    })
