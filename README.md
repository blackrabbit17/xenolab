## Xenolab - Rasp Pi monitor for my pet carnivourus plants

### Xenolab Running
-----------------------


### Why?
-----------------------
I wanted to have some fun with 3D printing and electronics, which gets me away from my normal day job running Atomic Tessellator (https://atomictessellator.com). There are lots of aspects of this project that are wildly impractical and over-engineered and done just for fun.




#### Electrical components
-----------------------
| Intel & Control | Atmospherics | Temp + Moisture |
|:--------------:|:---:|:-----------------:|
| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/usb-relay/USBPWR_RELAY_preview.png)<br>[USB Relay](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/subcomponents/usb-relay)<br/>USBPOWRL001    |![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/LED-lighting/XC4385_preview.png)<br>[Sunlight Simulation](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/subcomponents/LED-lighting)<br/>XC4380 24RGB |![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/temp-humidity/Y2163753_preview.png)<br>Temp + Humidity <br/>DHT11 v2|
| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/camera/SEVRBP0544__5_preview.png)<br>Camera<br/>12.3 MP Sony IMX500       |![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/50mm-fan/XC5055_preview.png)<br>Wind Simulation<br/>50mm 12V DC Fan| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/soil-moisture/LM393_preview.png)<br/>Soil Moisture<br/>LM393 |

<br/><br/>

#### Computing
-----------------------
| [Rasp-pi 5](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/computing/rasp-pi-5) | [Cooling Hat](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/computing/cooling-hat) | [Display](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/computing/display) |
|:--------------:|:---:|:-----------------:|
| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/computing/rasp-pi-5/pi5_preview.png)<br/>R-Pi 5 - 8GB<br/>Quad Core 2.4GHz<br/>ARM Cortex-A76 | ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/computing/cooling-hat/cooling-hat_preview.png)<br/>R-Pi 5<br/>RGB Cooling Hat<br/>w/ OLED Display | ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/computing/display/dfrobot-7in-800x480_preview.png)<br/>7" 800x480<br/>DSI Capacitive<br/>Touchscreen

<br/><br/>
#### CAD + Physical Design
-----------------------

<br/><br/>
### Build Pics
-----------------------

<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/construction_pics/IMG_5546.jpg" width="500">

Setting up the RASP Pi 5s and testing some sensors

<br/>

<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/construction_pics/3dprinted.png" width="500">

Fresh from the 3D printer!

<br/>

<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/construction_pics/FA9DE0F2-8E53-48A8-A0B5-AE390EFE8164.JPG" width="500">

Coated in black because it looks better

<br/>

<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/construction_pics/IMG_5797.jpg" width="500">

Starting to wire up the relays and power and sensors

<br/>

<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/construction_pics/IMG_5815.jpg" width="500">

Power-on tests

<br/>

<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/construction_pics/PHOTO-2025-05-06-14-32-45.jpg" width="500">

Sensor integration tests

