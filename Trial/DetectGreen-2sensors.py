#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch

ev3 = EV3Brick()
watch = StopWatch()

color1 = ColorSensor(Port.S1)
color2 = ColorSensor(Port.S2)

class ColorRawValue:
    def __init__(self,port):
        self.port = port

    def hsv(self):
        try:
            rgb_ = color1.rgb() if self.port == 1 else color2.rgb()
            rgb = rgb_[0] * (255 / 100), rgb_[1] * (255 / 100), rgb_[2] * (255 / 100)

            # Hue
            if rgb[1] < rgb[0] > rgb[2]: # Red
                hue = 60 * ((rgb[1] - rgb[2]) / (max(rgb) - min(rgb)))
            elif rgb[0] < rgb[1] > rgb[2]: # Green
                hue = 60 * ((rgb[2] - rgb[0]) / (max(rgb) - min(rgb))) + 120
            else: # Blue
                hue = 60 * ((rgb[0] - rgb[1]) / (max(rgb) - min(rgb))) + 240

            if hue < 0:
                hue += 360

            # Saturation
            saturation = (max(rgb) - min(rgb)) / max(rgb) * 100

            # Value
            value_brightness = max(rgb)

            return hue, saturation, value_brightness

        except TypeError as error:
            ev3.speaker.say(str(error))

        except ZeroDivisionError as error:
            ev3.speaker.say(str(error))

    def reflection(self):
        try:
            rgb_ = color1.rgb() if self.port == 1 else color2.rgb()
            return rgb_[0]

        except TypeError as error:
            ev3.speaker.say(str(error))

        except ZeroDivisionError as error:
            ev3.speaker.say(str(error))

    def ambinet(self):
        try:
            rgb_ = color1.rgb() if self.port == 1 else color2.rgb()
            return rgb_[2]

        except TypeError as error:
            ev3.speaker.say(str(error))

        except ZeroDivisionError as error:
            ev3.speaker.say(str(error))

color1 = ColorRawValue(1)
color2 = ColorRawValue(2)

hsv_ = color.hsv()

if 90 < hsv_[0] < 150 and 40 < hsv_[1] and 40 < hsv_[2]:
    ev3.speaker.say("green")
else:
    ev3.speaker.say("others")