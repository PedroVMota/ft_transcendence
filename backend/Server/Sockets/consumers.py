# Sockets/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer


class Menssage():
    def __init__(self, msg) -> None:
        self._HANDSHAKE = 'handshake' + msg
        self._MESSAGE = 'message' + msg
        self._ERROR = 'error' + msg
        self._SUCCESS = 'success' + msg
        self._CLOSE = 'close' + msg
        self._data = None
        

class YourConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(Menssage('Connected! ')._HANDSHAKE)
        

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            print(text_data_json)
            message = text_data_json['message']
            print(Menssage(message)._MESSAGE)
            self.send(text_data=json.dumps({
                'user': 'Server',
                'message': message
            }))
        except Exception as e:
            print(Menssage(str(e))._ERROR)
            self.send(text_data=json.dumps({
                'Error': str(e)
            }))
        