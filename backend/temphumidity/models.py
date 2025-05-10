from django.db import models
from django.utils import timezone


class TempHumidityReading(models.Model):
    """
    Model representing a temperature and humidity reading from a sensor
    """
    timestamp = models.DateTimeField(default=timezone.now)
    temperature = models.FloatField(help_text="Temperature value in Celsius")
    humidity = models.FloatField(help_text="Humidity value in percentage")
    
    def __str__(self):
        return f"Humidity: {self.value}%, Temp: {self.temperature}°C at {self.timestamp}"
