from django.db import models
from django.utils import timezone


class Wind(models.Model):
    """
    Model representing a wind reading from a sensor
    """
    
    STATUS_WIND_OFF = 0
    STATUS_WIND_ON = 1
    
    STATUS_CHOICES = [
        (STATUS_WIND_OFF, 'Off'),
        (STATUS_WIND_ON, 'On'),
    ]
    
    timestamp = models.DateTimeField(default=timezone.now)
    speed = models.FloatField(help_text="Wind speed value in m/s", default=0.2)
    status = models.IntegerField(help_text="Wind status value", choices=STATUS_CHOICES, default=STATUS_WIND_OFF)
    
    def __str__(self):
        return f"Wind: {self.speed} m/s, Status: {self.status} at {self.timestamp}"
