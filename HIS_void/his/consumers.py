from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models.signals import post_save
import json


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        data = [
            {
                "name": "李国铭",
                "ststus": "危机",
            },
        ]
        await self.send(json.dumps(data))

    async def send_inspecting_patient(self, sender, **kwargs):
        print("==========【调用send_inspecting_patient】=================")
        print(kwargs)
        # await self.accept()
        data = [
            {
                "name": "朱元琛",
                "ststus": "安全",
            },
        ]
        await self.send(json.dumps(data))


post_save.connect(WSConsumer().send_inspecting_patient)
