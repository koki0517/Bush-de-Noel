#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait, StopWatch

left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

watch = StopWatch()

def SpeedPercent(percentage):
    ''' percentageをdeg/sに変換します'''
    return 990 * percentage / 100
    # Lモーターの最大回転数が960~1020deg/sなのでその平均の990を最大回転数(deg/s)として採用しています。

class Tank:
    def steering(self,power,steering):
        if -100 > power or 100 > power:
            raise ValueError
        if -100 <= steering < 0:
            left_motor.run(SpeedPercent((power / 50) * steering + power)) # 式①
            right_motor.run(SpeedPercent(power)) # 式②
        elif 0 <= steering <= 100:
            left_motor.run(SpeedPercent(power)) # 式③
            right_motor.run(SpeedPercent(-1 * (power / 50) * steering + power)) # 式④
        else:
            raise ValueError

    def steering_for_seconds(self,power,steering,seconds,stop_type = "hold"):
        if seconds <= 0:
            raise ValueError
        time_run = watch.time() + seconds
        while watch.time() <= time_run:
            self.steering(power,steering)
        self.stop(stop_type)

    def steeing_for_degrees(self,power,steering,degrees,stop_type = "hold"):
        '''EV3-Gにおけるステアリングの「角度」「回転数」モードは左右2つのモーターのどちらかの変化量が
            指定した角度や回転数を超えるまで走るという内容になります。'''
        if degrees < 0:
            degrees *= -1
            steering *= -1
        left_angle = left_motor.angle()
        right_angle = right_motor.angle()
        while not abs(left_angle - left_motor.angle()) > degrees or abs(right_angle - right_motor.angle()) > degrees:
            self.steering(power,steering)
        self.stop(stop_type)

    def steering_for_rotations(self,power,steering,rotations,stop_type = "hold"):
        self.steeing_for_degrees(power,steering,rotations * 360)
        self.stop(stop_type)

    def stop(self,stop_type):
        if stop_type == "stop":
            left_motor.stop()
            right_motor.stop()
        elif stop_type == "brake":
            left_motor.brake()
            right_motor.brake()
        elif stop_type == "hold":
            left_motor.hold()
            right_motor.hold()
        else:
            raise ValueError

tank = Tank()

# 50%のパワーで10秒間右旋回する
tank.steering_for_seconds(50,100,10)

# 40%のパワーで1024度モーターが回転するまで右スピン
tank.steeing_for_degrees(40,50,1024)

# 70%のパワーでモーターが3回転するまで左斜め前に走る
tank.steering_for_rotations(70,-20,3)
