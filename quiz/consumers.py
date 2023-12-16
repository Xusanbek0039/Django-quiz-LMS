from channels.generic.websocket import AsyncWebsocketConsumer
import json


class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('group_layer', self.channel_name)
        await self.accept()



    async def disconnect(self, code):
        await self.channel_layer.group_discard('group_layer', self.channel_name)


    async def send_interval_group(self, event):
        date_now = event['message']
        await self.send(json.dumps({'quiz_start': date_now}))
