#!/usr/bin/env python3
import time
import sys

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound

arm = MediumMotor(OUTPUT_A)
left_motor = LargeMotor(OUTPUT_B)
right_motor = LargeMotor(OUTPUT_C)

tank = MoveTank(OUTPUT_B,OUTPUT_C)
steering = MoveSteering(OUTPUT_B,OUTPUT_C)

left_color = ColorSensor(INPUT_1)
right_color = ColorSensor(INPUT_2)

classify_color = ColorSensor(INPUT_3)

class PID:
    Kp = 0.1
    middle = 35

    def on(self,base_speed,direction):
        if direction == "left":
            u = PID.Kp * (PID.middle - left_color.color)
        else:
            u = PID.Kp * (left_color.color - PID.middle)
        tank.on(-1*(base_speed - u), -1*(base_speed + u))

class MoveArm:
    '''control the arm
        基本の状態はアームを下げて閉じる'''

    def hold(self):
        '''アームが下がり、"開いてる"状態からアームを閉じる'''

    def release(self):
        '''アームが下がり、"閉じている"状態からアームを開く'''

    def raise_arm(self):
        '''アームが下がっている状態から、アームを上げる'''
        arm.on_for_degrees(40,120,False) #初速度をつける
        while arm.speed() > 30:
            arm.on(40)
        arm.on_for_seconds(40,0.5,False)
        arm.stop("coast")
        time.sleep(1)

    def lower_arm(self):
        '''アームが上がっている状態から、アームを下げる'''
        arm.on_for_degrees(-40,100,False)
        while arm.speed() < -30:
            arm.on(40)
        arm.stop("hold")

    def ball(self):
        '''ボールを上げて落とす
            アームは上げっぱなし'''
        self.raise_arm()
        arm.on_for_degrees(-20,100,False)
