from django.db import models
from django.utils import timezone


class Sunlight(models.Model):
    """
    Model representing a sunlight reading from a sensor
    """
    
    STATUS_SUNLIGHT_OFF = 0
    STATUS_SUNLIGHT_ON = 1
    
    STATUS_CHOICES = [
        (STATUS_SUNLIGHT_OFF, 'Off'),
        (STATUS_SUNLIGHT_ON, 'On'),
    ]
    
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(help_text="Sunlight status value", choices=STATUS_CHOICES, default=STATUS_SUNLIGHT_OFF)
    
    r = models.FloatField(help_text="Red component of sunlight", default=0.2)
    g = models.FloatField(help_text="Green component of sunlight", default=0.2)
    b = models.FloatField(help_text="Blue component of sunlight", default=0.2)
    
    brightness = models.FloatField(help_text="Brightness of sunlight", default=0.8)
    
    def __str__(self):
        return f"Sunlight: r={self.r}, g={self.g}, b={self.b}, brightness={self.brightness} at {self.timestamp}"
