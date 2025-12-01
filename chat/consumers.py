import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from chat.models import ChatMessage,Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.user = self.scope['user']
        self.room_group_name = f'chat_{self.room_name}'

        #Join room group
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)

        await self.accept()

    async def disconnect(self,closed_code):
        #leave room group
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    @database_sync_to_async
    def persist_message(self,message):
        active_room = Room.objects.get(name=self.room_name)
        ChatMessage.objects.create(room=active_room,sender=self.user,message=message)

    #receive message from websocket
    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = self.user.username
        #send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat.message",
                "message":message,
                "username":username
            }
        )
        await self.persist_message(message)

    async def chat_message(self,event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({'message':message,'username':username}))
    