### USBPOWRL001 - USB Relay
---------------------------

![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/usb-relay/USBPWR_RELAY.png)


### Sample Code
- Switch both relays ON
- Wait 5 seconds
- Switch both relays OFF
```
import serial
import time
 
def send_command(ser_port, command):
    """Send command to the serial port and read the response."""
    ser_port.write(command.encode())
    time.sleep(1)
    response = ser_port.read(25).decode()
    return response
 
def main():
    port_name = "/dev/ttyACM0"  # Replace with your actual COM port
    baud_rate = 19200
    timeout = 5
 
    try:
        with serial.Serial(port_name, baud_rate, timeout=timeout) as ser_port:

            for relay_number in [1, 2]:
                relay_on_command = f"relay on {relay_number}\r"
                print(f"Relay {relay_number} ON ...", end="", flush=True)
                send_command(ser_port, relay_on_command)
                print("OK")

            time.sleep(5)

            for relay_number in [1, 2]:
                relay_clear_command = f"relay off {relay_number}\r"
                print(f"Relay {relay_number} OFF ...", end="", flush=True)
                send_command(ser_port, relay_clear_command)
                print("OK")

            
    except serial.SerialException as e:
        print(f"Error opening or communicating with serial port: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
 
if __name__ == "__main__":
    main()
```