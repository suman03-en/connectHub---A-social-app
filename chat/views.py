from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

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
    room_ids = [int(id) for id in room_name.split("-")[1:]]
    other_user_id = [id for id in room_ids if id!=request.user.id]
    other_user = get_user_model().objects.get(id=other_user_id[0])
    obj, created = Room.objects.get_or_create(name=room_name)
    obj.participants.add(request.user,other_user)
    latest_messages = obj.messages.all()
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "latest_messages": latest_messages
    })

@login_required(login_url='login')
def message_box(request):
    current_user = request.user
    user_rooms = current_user.rooms.all()
    return render(
        request,
        "chat/message/list.html",
        {
            'user_rooms':user_rooms
        }
    )
