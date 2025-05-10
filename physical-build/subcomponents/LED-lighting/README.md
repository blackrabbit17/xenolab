### XC4380 24RGB - Sunlight simulation
-----------------------

![](https://raw.githubusercontent.com/blackrabbit17/xenolab/refs/heads/main/physical-build/subcomponents/LED-lighting/XC4385.png)




> [Manual Here](https://github.com/blackrabbit17/xenolab/blob/79a7be1f56b2e6669d1301d31d983a958c4328d6/physical-build/subcomponents/LED-lighting/XC4385_manualMain_93994.pdf) (including wiring diagram)<br/><br/>Note that you only need to connect Dout (and the VCC and GND near the Dout) if you are daisy chaining
multiple units together, This functionality is not used in xenolab, so these wires are removed, and the only wires we used are `Din`, `VCC` and `Gnd`

### Sample Code
```
import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D12, 24, brightness=1.0, auto_write=True)

pixels.fill((255, 255, 255))   # On - pure white color

time.sleep(5)

pixels.fill((0, 255, 0))       # On - pure green color

time.sleep(5)

pixels.fill((0, 0, 0))         # Off
```

### Sample Code - Pride Weekend
```
import board
import neopixel
import time
import math
import colorsys

pixels = neopixel.NeoPixel(board.D12, 24, auto_write=False)

while True:
    for hue in range(360):
        for i in range(len(pixels)):
            brightness = (math.sin(time.time() * 3 + i) + 1) / 2
            pixels.brightness = brightness * 2.5 + 0.1
            rgb_float = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
            rgb = tuple(int(c * 255) for c in rgb_float)
            pixels[i] = rgb
        pixels.show()
        time.sleep(0.01)
```