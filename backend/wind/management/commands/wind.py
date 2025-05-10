from django.core.management.base import BaseCommand
from django.utils import timezone
from wind.models import Wind

import os
import serial
import time
import datetime
from zoneinfo import ZoneInfo

import loguru

class Command(BaseCommand):
    help = 'Control wind system - on at 8:00am and off at 8:00pm daily'

    def handle(self, *args, **kwargs):
        loguru.logger.info("Starting wind worker")

        port_name = os.environ.get("XENOLAB_WIND_PORT", "/dev/ttyACM0")
        baud_rate = os.environ.get("XENOLAB_WIND_BAUD_RATE", 19200)
        timeout = os.environ.get("XENOLAB_WIND_TIMEOUT", 5)
        
        wind_relay = os.environ.get("XENOLAB_WIND_RELAY", 1)
        RELAY_ON_COMMAND = f"relay on {wind_relay}\r"
        RELAY_OFF_COMMAND = f"relay off {wind_relay}\r"

        ser_port = serial.Serial(port_name, baud_rate, timeout=timeout)
        
        loguru.logger.info(f"Worker starting up with port {port_name} and baud rate {baud_rate} and timeout {timeout}")

        # Keep track of current state and last change dates
        wind_is_on = False

        while True:
            now = datetime.datetime.now(ZoneInfo(os.environ.get("XENOLAB_TIMEZONE", "Pacific/Auckland")))
            current_time = now.time()
            
            # Morning check (8:00am)
            if current_time.hour >= 8 and current_time.hour < 20:
                # Check if we haven't turned on yet today
                if not wind_is_on:
                    loguru.logger.info(f"Turning wind on at {now.strftime('%H:%M:%S')}")

                    response = self.send_command(ser_port, RELAY_ON_COMMAND)
                    loguru.logger.info(f"Wind turned ON at {now.strftime('%H:%M:%S')}")
                    wind_is_on = True
                    
                    # Record wind on in database
                    Wind.objects.create(
                        timestamp=timezone.now(),
                        status=Wind.STATUS_WIND_ON
                    )
                else:
                    loguru.logger.info(f"Wind is already on at {now.strftime('%H:%M:%S')}")

            # Evening check (8:00pm): Turn off if not already off today
            if current_time.hour >= 20 or current_time.hour < 8:
                # Check if we haven't turned off yet today
                if wind_is_on:
                    loguru.logger.info(f"Turning wind off at {now.strftime('%H:%M:%S')}")

                    response = self.send_command(ser_port, RELAY_OFF_COMMAND)
                    loguru.logger.info(f"Wind turned OFF at {now.strftime('%H:%M:%S')}")
                    wind_is_on = False
                    
                    # Record wind off in database
                    Wind.objects.create(
                        timestamp=timezone.now(),
                        status=Wind.STATUS_WIND_OFF
                    )
                else:
                    loguru.logger.info(f"Wind is already off at {now.strftime('%H:%M:%S')}")

            # Sleep for 60 seconds before checking again
            time.sleep(60)
    
    def send_command(self, ser_port, command):
        """Send command to serial port and return response"""
        ser_port.write(command.encode())
        time.sleep(0.5)
        response = ser_port.readline().decode().strip()
        return response
