from asgiref.sync import async_to_sync
from channels.generic.websocket import cWebsocketConsumer
import json
from .models import Message

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print('fetch')
        pass
    
    def new_message(self, data):
        print('new message')
        pass 

    commands = {
        'fetch_messages':fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']][self,data]


    def send_cat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        async_to_sync(self.send(text_data=json.dumps({
            'message': message
        })))