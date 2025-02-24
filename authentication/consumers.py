import json
from channels.generic.websocket import WebsocketConsumer
from .models import SensorData

class SensorDataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        if 'error' in data:
            self.send(text_data=json.dumps({
                'error': data['error']
            }))
        elif 'success' in data:
            self.send(text_data=json.dumps({
                'success': data['success']
            }))
        else:
            sensor_data = SensorData.objects.create(
                temperature=data['temperature'],
                humidity=data['humidity'],
                luminosity=data['luminosity'],
                is_connected=True
            )
            self.send(text_data=json.dumps({
                'temperature': sensor_data.temperature,
                'humidity': sensor_data.humidity,
                'luminosity': sensor_data.luminosity,
                'timestamp': sensor_data.timestamp.isoformat()
            }))