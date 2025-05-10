# gThumb-PiWare: Smart Plant Monitoring System

## Overview
gThumb-PiWare is an open-source firmware layer for Raspberry Pi devices that transforms your Pi into an intelligent plant monitoring and care system. Originally designed for carnivorous plants, this system works with all types of plants that need precise environmental control.

![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/finished.jpg)

![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/frontend/screenshot.png)

## For Non-Technical Users

### What This Does
gThumb-PiWare turns your Raspberry Pi into a smart gardening assistant that:
- Monitors temperature and humidity around your plants
- Creates perfect lighting conditions with programmable LED lights
- Simulates natural air movement with gentle fan control
- Tracks soil moisture to help prevent over/under watering
- Takes photos of your plants to track growth
- Displays all information on a touchscreen dashboard

### Getting Started (Pre-built Kit)
If you purchased a pre-built kit:

1. Place the device near your plants
2. Connect the soil moisture sensors (the metal prongs) into your plant pots
3. Plug in the power supply
4. The touchscreen will turn on automatically
5. Follow the on-screen instructions to connect to your WiFi
6. Use the touchscreen to set up your plant types and care routines

### Troubleshooting
- If the screen doesn't turn on, check the power connection
- If sensors aren't showing readings, make sure they're properly connected
- For additional help, visit support.gthumb.ai or email help@gthumb.ai

## For Technical Users

### System Features
- Raspberry Pi 5 based system (also works with Pi 4)
- 7" 800x480 Touchscreen interface
- Temperature & Humidity monitoring via DHT11 sensors
- Programmable RGB LED lighting (24 LEDs for complete spectrum control)
- Fan control for air circulation
- Soil moisture sensors with LM393 comparators
- USB relay control system for all peripherals
- Camera integration for plant monitoring and timelapse
- Django backend with Vue.js frontend

### Setup Instructions

#### Hardware Requirements
- Raspberry Pi 4 or 5 with at least 4GB RAM
- Compatible sensors (see [Electrical Components](#electrical-components) section)
- 7" DSI touchscreen (recommended) or regular monitor

#### Software Installation
```bash
# Clone the repository
git clone https://github.com/gthumb/piware.git
cd piware

# Install backend dependencies
cd backend
pip install -r requirements.txt
python manage.py migrate

# Install frontend dependencies
cd ../frontend
npm install
```

#### Running the System
```bash
# Start backend server
cd backend
python manage.py runserver

# In a new terminal, start frontend
cd frontend
npm run dev
```

For production deployment:
```bash
# Build frontend
cd frontend
npm run build

# Run backend in production mode
cd ../backend
python manage.py runserver 0.0.0.0:8000
```

### Backend Testing
To run the backend tests:

```bash
# Run all tests
cd backend && python manage.py test

# Run tests for a specific app
cd backend && python manage.py test sunlight

# Run tests for a specific test class
cd backend && python manage.py test app_name.tests.TestClass
```

### Environmental Simulation
The system includes commands to simulate natural conditions:

```bash
# Simulate sunlight patterns
cd backend && python manage.py sunlight

# Simulate wind patterns
cd backend && python manage.py wind

# Record temperature and humidity
cd backend && python manage.py temphumidity
```

## Electrical Components
| Intel & Control | Atmospherics | Temp + Moisture |
|:--------------:|:---:|:-----------------:|
| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/usb-relay/USBPWR_RELAY_preview.png)<br>[USB Relay](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/subcomponents/usb-relay)<br/>USBPOWRL001    |![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/LED-lighting/XC4385_preview.png)<br>[Sunlight Simulation](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/subcomponents/LED-lighting)<br/>XC4380 24RGB |![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/temp-humidity/Y2163753_preview.png)<br>Temp + Humidity <br/>DHT11 v2|
| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/camera/SEVRBP0544__5_preview.png)<br>Camera<br/>12.3 MP Sony IMX500       |![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/50mm-fan/XC5055_preview.png)<br>Wind Simulation<br/>50mm 12V DC Fan| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/soil-moisture/LM393_preview.png)<br/>Soil Moisture<br/>LM393 |

## Computing
| [Rasp-pi 5](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/computing/rasp-pi-5) | [Cooling Hat](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/computing/cooling-hat) | [Display](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/computing/display) |
|:--------------:|:---:|:-----------------:|
| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/computing/rasp-pi-5/pi5_preview.png)<br/>R-Pi 5 - 8GB<br/>Quad Core 2.4GHz<br/>ARM Cortex-A76 | ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/computing/cooling-hat/cooling-hat_preview.png)<br/>R-Pi 5<br/>RGB Cooling Hat<br/>w/ OLED Display | ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/computing/display/dfrobot-7in-800x480_preview.png)<br/>7" 800x480<br/>DSI Capacitive<br/>Touchscreen

## CAD + Physical Design
The enclosure design files are available in the repository for 3D printing your own housing.

<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/CAD/main_housing/preview2.png" width="383">
<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/CAD/main_housing/preview1.png" width="250">

[Main Housing Model File](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/CAD/main_housing)

<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/CAD/fan_housing/preview.png" width="383">

[Fan Housing Model File](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/CAD/fan_housing)

## License
This project is open source under the MIT License. See the LICENSE file for details.

## Contributing
We welcome contributions from the community! Please see CONTRIBUTING.md for guidelines.

## Support
For help and support:
- Technical issues: Create an issue on GitHub
- General questions: Visit [support.gthumb.ai](https://support.gthumb.ai)
- Email: help@gthumb.ai