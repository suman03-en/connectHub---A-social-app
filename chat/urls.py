from django.urls import path

from . import views


urlpatterns = [
    path("",views.index,name="index"),
    path("inbox/",views.message_box,name="message_box"),
    path("<str:room_name>/",views.room,name='room'),
]
