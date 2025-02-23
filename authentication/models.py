from django.db import models
from django.utils import timezone

class SensorData(models.Model):
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    luminosity = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_connected = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Sensor Data at {self.timestamp}"

    @classmethod
    def get_latest(cls):
        return cls.objects.first()
