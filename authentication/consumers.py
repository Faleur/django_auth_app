import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.utils import timezone
from .models import SensorData

class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "sensors",
            self.channel_name
        )
        await self.accept()
        
        # Envoyer l'état initial
        latest_data = await self.get_latest_data()
        if latest_data:
            await self.send(text_data=json.dumps({
                'type': 'sensor_data',
                'data': latest_data
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "sensors",
            self.channel_name
        )
        # Marquer comme déconnecté
        await self.update_connection_status(False)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            sensor_data = {
                'temperature': text_data_json.get('temperature'),
                'humidity': text_data_json.get('humidity'),
                'luminosity': text_data_json.get('luminosity'),
                'timestamp': timezone.now().isoformat(),
                'is_connected': True
            }

            # Sauvegarder les données
            await self.save_sensor_data(sensor_data)

            # Broadcast à tous les clients connectés
            await self.channel_layer.group_send(
                "sensors",
                {
                    'type': 'sensor_update',
                    'data': sensor_data
                }
            )

        except json.JSONDecodeError:
            print("Invalid JSON format received")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    async def sensor_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def save_sensor_data(self, data):
        SensorData.objects.create(
            temperature=data['temperature'],
            humidity=data['humidity'],
            luminosity=data['luminosity'],
            is_connected=True
        )

    @database_sync_to_async
    def get_latest_data(self):
        latest = SensorData.get_latest()
        if latest:
            return {
                'temperature': latest.temperature,
                'humidity': latest.humidity,
                'luminosity': latest.luminosity,
                'timestamp': latest.timestamp.isoformat(),
                'is_connected': latest.is_connected
            }
        return None

    @database_sync_to_async
    def update_connection_status(self, status):
        latest = SensorData.get_latest()
        if latest:
            latest.is_connected = status
            latest.save()
