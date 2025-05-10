## Xenolab - Rasp Pi monitor for my pet carnivorous plants
The Xenolab Rasp Pi Monitor is a cutting-edge, semi-autonomous biosurveillance module engineered for the precise care and observation of exotic carnivorous flora. 

> <br/>
> ⚠️ WARNING: MONITORING TRIFFIDS<br/><br/>
> The Xenolab Rasp Pi Monitor is not certified for use with Triffids or other semi-sentient, ambulatory flora. Historical data suggests a high incidence of operator attrition and catastrophic habitat compromise when engaging with such species. While the system may successfully log preliminary biometric data, prolonged monitoring is statistically correlated with acute reductions in observer longevity.<br/>— Xenolab Safety Directive 12.4B<br/><br/>



### Xenolab Running
-----------------------

![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/finished.jpg)

It's just past 8AM so it's about 50% though simulated sunrise.

![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/frontend/screenshot.png)

Main features:
- Rasp Pi 5
- 7" 800x480 Touchscreen
- Temperature Monitor
- Humidity Monitor
- Fan to simulate wind
- 24 R,G,B LED for light
- Soil Moisture Sensor
- USB relays so the Rasp Pi can control all of the sensors / fans etc


### Why?
-----------------------
I wanted to have some fun with 3D printing and electronics, which gets me away from my normal day job running Atomic Tessellator (https://atomictessellator.com). There are lots of aspects of this project that are wildly impractical and over-engineered and done just for fun.

### Electrical components
-----------------------
| Intel & Control | Atmospherics | Temp + Moisture |
|:--------------:|:---:|:-----------------:|
| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/usb-relay/USBPWR_RELAY_preview.png)<br>[USB Relay](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/subcomponents/usb-relay)<br/>USBPOWRL001    |![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/LED-lighting/XC4385_preview.png)<br>[Sunlight Simulation](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/subcomponents/LED-lighting)<br/>XC4380 24RGB |![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/temp-humidity/Y2163753_preview.png)<br>Temp + Humidity <br/>DHT11 v2|
| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/camera/SEVRBP0544__5_preview.png)<br>Camera<br/>12.3 MP Sony IMX500       |![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/50mm-fan/XC5055_preview.png)<br>Wind Simulation<br/>50mm 12V DC Fan| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/soil-moisture/LM393_preview.png)<br/>Soil Moisture<br/>LM393 |

<br/>

### Computing
-----------------------
| [Rasp-pi 5](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/computing/rasp-pi-5) | [Cooling Hat](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/computing/cooling-hat) | [Display](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/computing/display) |
|:--------------:|:---:|:-----------------:|
| ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/computing/rasp-pi-5/pi5_preview.png)<br/>R-Pi 5 - 8GB<br/>Quad Core 2.4GHz<br/>ARM Cortex-A76 | ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/computing/cooling-hat/cooling-hat_preview.png)<br/>R-Pi 5<br/>RGB Cooling Hat<br/>w/ OLED Display | ![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/computing/display/dfrobot-7in-800x480_preview.png)<br/>7" 800x480<br/>DSI Capacitive<br/>Touchscreen

<br/>

### CAD + Physical Design
-----------------------
I'm really new at CAD, this was my first time. It's ok, you can laugh at my designs.

I used the wonderful [tinkercad.com]() because I found that to be the most intuitive.

```
I can code in my sleep, make logic unfold,
But hand me some CAD and my courage turns cold.
Lines go zig when they clearly should zag,
My blueprints look more like a digital gag.
```
<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/CAD/main_housing/preview2.png" width="383">
<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/CAD/main_housing/preview1.png" width="250">

[Model File](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/CAD/main_housing)

<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/CAD/fan_housing/preview.png" width="383">

[Model File](https://github.com/blackrabbit17/xenolab/tree/main/physical-build/CAD/fan_housing)

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

<img src="https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/construction_pics/IMG_5913.jpg" width="500">

Finished connecting all the sensors up


![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/finished.jpg)

Finished and running!
