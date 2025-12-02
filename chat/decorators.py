from functools import wraps
from django.http import HttpResponse



def room_owner_required(view_func):

    @wraps(view_func)
    def wrapper(request,room_name):
        current_user_id = str(request.user.id)
        room_id = room_name.split("-")[1:]
        if current_user_id in room_id:
            return view_func(request,room_name)
        else:
            return HttpResponse("Private room")
    return wrapper
