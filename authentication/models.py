from django.db import models

class SensorData(models.Model):
    temperature = models.FloatField(default=0.0)  # Ajout d'une valeur par défaut
    humidity = models.FloatField(default=0.0)     # Ajout d'une valeur par défaut
    luminosity = models.FloatField(default=0.0)   # Ajout d'une valeur par défaut
    soilHumidity = models.FloatField(default=0.0)  # Ajout du champ soilHumidity
    timestamp = models.DateTimeField(auto_now_add=True)
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return f"SensorData({self.temperature}, {self.humidity}, {self.luminosity}, {self.soilHumidity}, {self.timestamp})"

    @classmethod
    def get_latest(cls):
        return cls.objects.latest('timestamp')