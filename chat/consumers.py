import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        '''self.scope is like req.user'''
        self.room_id = self.scope[
            "url_route"
        ]["kwargs"]["room_id"]

        self.room_group_name = (
            f"chat_{self.room_id}"
        )
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        print(f"connected:{self.scope['user']}")
        await self.accept()

    async def disconnect(self,close_code,):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        print(f"disconnected:{close_code}")

    async def receive(self,text_data,):
        data = json.loads(text_data)
        message = data["message"]
        user = self.scope["user"]

        await self.save_message(
            user,
            message
        )

        print("receive called")
        '''buyer send msg'''

        '''this data(msg) goes to consumer-->redis-->group nd then redis knows that room nd send msg to every connection'''
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": user.username,
            },
        )

        # await self.send(text_data=json.dumps(
        #     {
        #         'message':message,
        #         "sender":user.username
        #     }
        # ))
        print("group send done")
        '''msg send to redis group'''

    async def chat_message(self,event,):
        print("chat msg called")
        '''redis send event to all user in room'''
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "sender": event["sender"],
                }
            )
        )
        print("msg sent to browser")

    @database_sync_to_async
    def save_message(self,user,message):
        room = ChatRoom.objects.get(
            id=self.room_id
        )
        Message.objects.create(
            room=room,
            sender=user,
            message=message
        )

        