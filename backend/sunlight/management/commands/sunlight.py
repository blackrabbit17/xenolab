from django.core.management.base import BaseCommand
from sunlight.models import Sunlight
from django.utils import timezone
import board
import neopixel
import time
import datetime
import math
from zoneinfo import ZoneInfo
import os


class Command(BaseCommand):
    help = 'Sunlight simulator with sunrise and sunset transitions'
    
    def handle(self, *args, **kwargs):
        # Initialize the NeoPixel strip
        pixels = neopixel.NeoPixel(board.D12, 24, brightness=0.9, auto_write=True)
        self.stdout.write(self.style.SUCCESS('Starting sunlight simulation'))
        
        last_record_time = None
        
        try:
            while True:
                now = datetime.datetime.now(ZoneInfo(os.environ.get("XENOLAB_TIMEZONE", "Pacific/Auckland")))
                current_time = now.time()
                
                # SUNRISE: 8:00AM to 9:00AM
                if datetime.time(8, 0) <= current_time < datetime.time(9, 0):
                    minutes_into_sunrise = (now.hour - 8) * 60 + now.minute
                    progress = minutes_into_sunrise / 60.0  # 0.0 to 1.0
                    
                    # Sunrise colors change from deep orange to bright white
                    r = min(255, int(255 * (0.8 + 0.2 * progress)))
                    g = min(255, int(255 * (0.3 + 0.7 * progress)))
                    b = min(255, int(255 * (0.1 + 0.9 * progress)))
                    brightness = 0.3 + (0.7 * progress)
                    
                    pixels.brightness = brightness
                    pixels.fill((r, g, b))
                    
                    # Save data every minute during sunrise
                    self._record_data(r/255.0, g/255.0, b/255.0, brightness, Sunlight.STATUS_SUNLIGHT_ON)
                    
                # DAYTIME: 9:00AM to 6:00PM
                elif datetime.time(9, 0) <= current_time < datetime.time(18, 0):
                    # Hours into daytime (0 to 9)
                    hours_into_day = (now.hour - 9) + (now.minute / 60.0)
                    
                    # Brightness curve: 0.3 → 1.0 → 0.3 over 9 hours
                    # Using a sine curve for smooth transition
                    brightness = 0.3 + 0.7 * math.sin(math.pi * hours_into_day / 9.0)
                    
                    pixels.brightness = brightness
                    pixels.fill((255, 255, 255))  # Full white
                    
                    # Record once per hour during daytime
                    current_hour = now.replace(minute=0, second=0, microsecond=0)
                    if last_record_time is None or (current_hour != last_record_time and now.minute < 5):
                        last_record_time = current_hour
                        self._record_data(1.0, 1.0, 1.0, brightness, Sunlight.STATUS_SUNLIGHT_ON)
                
                # SUNSET: 6:00PM to 7:00PM
                elif datetime.time(18, 0) <= current_time < datetime.time(19, 0):
                    minutes_into_sunset = (now.hour - 18) * 60 + now.minute
                    progress = minutes_into_sunset / 60.0  # 0.0 to 1.0
                    
                    # Sunset colors change from white to deep red/orange
                    r = min(255, int(255 * (1.0)))
                    g = min(255, int(255 * (1.0 - (0.7 * progress))))
                    b = min(255, int(255 * (1.0 - (0.9 * progress))))
                    brightness = 0.3 + (0.7 * (1.0 - progress))
                    
                    pixels.brightness = brightness
                    pixels.fill((r, g, b))
                    
                    # Save data every minute during sunset
                    self._record_data(r/255.0, g/255.0, b/255.0, brightness, Sunlight.STATUS_SUNLIGHT_ON)
                
                # NIGHT: Turn off lights
                else:
                    pixels.brightness = 0
                    pixels.fill((0, 0, 0))
                    
                    # Only record status change when transitioning to night
                    if last_record_time is None or (now - last_record_time).total_seconds() > 3600:
                        last_record_time = now
                        self._record_data(0, 0, 0, 0, Sunlight.STATUS_SUNLIGHT_OFF)
                
                # Wait for 1 second before next iteration
                time.sleep(1)
                
        except KeyboardInterrupt:
            # Clean up when exiting
            pixels.fill((0, 0, 0))
            self.stdout.write(self.style.SUCCESS('Sunlight simulation stopped'))
    
    def _record_data(self, r, g, b, brightness, status):
        """Record the current light settings to the database"""
        Sunlight.objects.create(
            r=r,
            g=g,
            b=b,
            brightness=brightness,
            status=status,
            timestamp=timezone.now()
        )
        self.stdout.write(f"Recorded: r={r:.2f}, g={g:.2f}, b={b:.2f}, brightness={brightness:.2f}, status={status}")
