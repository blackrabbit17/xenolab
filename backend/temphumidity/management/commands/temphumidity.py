from django.core.management.base import BaseCommand
from django.utils import timezone
from temphumidity.models import TempHumidityReading

import adafruit_dht
import board
import time
import datetime
import statistics

import loguru

class Command(BaseCommand):
    help = 'Read temperature and humidity from DHT11 sensor once an hour at minute 00'

    def handle(self, *args, **kwargs):
        loguru.logger.info("Starting temperature and humidity worker - hourly schedule at minute 00")
        # Initialize the DHT11 sensor
        dhtDevice = adafruit_dht.DHT11(board.D4)  # GPIO4 == board.D4

        while True:
            current_time = datetime.datetime.now()
            
            # Only take reading if the current minute is 00
            if True or current_time.minute == 0:
                temp_readings = []
                humidity_readings = []
                
                loguru.logger.info("Taking 10 readings to average...")
                
                # Take 10 readings with 1 second gap
                for i in range(10):
                    try:
                        temperature = dhtDevice.temperature
                        humidity = dhtDevice.humidity
                        
                        if temperature is not None and humidity is not None:
                            temp_readings.append(temperature)
                            humidity_readings.append(humidity)
                            loguru.logger.debug(f"Reading {i+1}/10: Temp={temperature}°C, Humidity={humidity}%")
                        
                    except Exception as e:
                        loguru.logger.error(f"Error on reading {i+1}: {e}")
                    
                    # Wait 1 second between readings
                    time.sleep(1)
                
                # Calculate averages if we have valid readings
                if temp_readings and humidity_readings:
                    avg_temp = statistics.mean(temp_readings)
                    avg_humidity = statistics.mean(humidity_readings)
                    
                    loguru.logger.info(f"Hourly reading (averaged from {len(temp_readings)} samples) - Temperature: {avg_temp:.1f}°C, Humidity: {avg_humidity:.1f}%")

                    # Create a new TempHumidityReading object with averaged values
                    reading = TempHumidityReading(
                        temperature=avg_temp,
                        humidity=avg_humidity
                    )
                    reading.save()
                else:
                    loguru.logger.error("Failed to get any valid readings in 10 attempts")
                
                # Sleep for 120 seconds to avoid multiple readings in the same hour
                time.sleep(120)
            else:
                # Check again in 10 seconds
                time.sleep(10)
