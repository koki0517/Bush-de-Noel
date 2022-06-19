#!/usr/bin/env pybricks-micropython
from tkinter import N
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Direction, Color, Button
from pybricks.tools import wait, StopWatch

watch = StopWatch()

color1 = ColorSensor(Port.S1)
color2 = ColorSensor(Port.S2)
color_detect = ColorSensor(Port.S3) # to detect a color of marking blocks

left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

def speed_precent(percentage):
    ''' percentageをdeg/sに変換'''
    return 990 * percentage / 100

class Tank:
    '''PID制御とMovetank,Movesteeringをまとめたclass'''
    # pid-control mode-----------------------------------------------------------------------------
    Kp = 1.2
    Ki = 0.5
    Kd = 1.0
    individual_difference = 0 #cs2-cs3
    errors = [0,0,0,0,0]

    def drive_pid(self, base_speed):
        '''drive under pid-control'''
        error = color1.refrection() - color2.refrection() - Tank.individual_difference
        Tank.errors.append(error)
        del Tank.errors[0]
        sum_control_amount = (Tank.Kp * error
                             + Tank.Ki * sum(Tank.errors)
                                 + Tank.Kd * (error - Tank.errors[-1]))
        left_motor.run(base_speed + sum_control_amount)
        right_motor.run(base_speed - sum_control_amount)

    def drive_pid_for_seconds(self, base_speed, time, stop_type = "hold"):
        '''drive under pid-control for specified seconds'''
        time_run = watch.time() + time
        while watch.time() <= time_run:
            self.drive_pid(base_speed)
        self.stop(stop_type)

    def drive_pid_for_degrees(self, base_speed, degrees, stop_type = "hold"):
        '''drive under pid-control for specified degrees'''
        left_angle = left_motor.angle()
        right_angle = right_motor.angle()
        while (not abs(left_angle - left_motor.angle()) > degrees
                    or abs(right_angle - right_motor.angle()) > degrees):
            self.drive_pid(base_speed)
        self.stop(stop_type)

    def drive_pid_for_rotations(self, base_speed, rotations, stop_type = "hold"):
        '''drive under pid-control for specified rotations'''
        self.drive_pid_for_degrees(base_speed,rotations * 360,stop_type)

    # tank mode------------------------------------------------------------------------------------
    def drive(self, left_speed, right_speed):
        '''just drive such as tank'''
        left_motor.run(speed_precent(left_speed))
        right_motor.run(speed_precent(right_speed))

    def drive_for_seconds(self, left_speed, right_speed, seconds, stop_type = "hold"):
        '''drive in tank for specified seconds'''
        left_motor.run_time(speed_precent(left_speed), seconds)
        left_motor.run_time(speed_precent(right_speed), seconds)
        wait(seconds * 1000)
        self.stop(stop_type)

    def drive_for_degrees(self, left_speed, right_speed, degrees, stop_type = "hold"):
        '''drive in tank for specified degrees'''
        left_angle = left_motor.angle()
        right_angle = right_motor.angle()
        while (not abs(left_angle - left_motor.angle()) > degrees
                    or abs(right_angle - right_motor.angle()) > degrees):
            left_motor.run(speed_precent(left_speed))
            right_motor.run(speed_precent(right_speed))
        self.stop(stop_type)

    def drive_for_rotations(self, left_speed, right_speed, rotations, stop_type = "hold"):
        '''drive in tank for specified rotations'''
        degrees = rotations * 360
        self.drive_for_degrees(left_speed,right_speed,degrees,stop_type)

    # steering mode--------------------------------------------------------------------------------
    def steering(self,power,steering):
        '''drive in steering forever'''
        if -100 > power or 100 > power:
            raise ValueError
        if -100 <= steering < 0:
            left_motor.run(speed_precent((power / 50) * steering + power)) # 式①
            right_motor.run(speed_precent(power)) # 式②
        else:
            left_motor.run(speed_precent(power)) # 式③
            right_motor.run(speed_precent(-1 * (power / 50) * steering + power)) # 式④

    def steering_for_seconds(self,power,steering,seconds,stop_type = "hold"):
        '''drive in steering for specified seconds'''
        if seconds <= 0:
            raise ValueError
        time_run = watch.time() + seconds
        while watch.time() <= time_run:
            self.steering(power,steering)
        self.stop(stop_type)

    def steering_for_degrees(self,power,steering,degrees,stop_type = "hold"):
        '''左右2つのモーターのどちらかの角度の変化量が指定した角度を超えるまでステアリングで走る'''
        if degrees < 0:
            degrees *= -1
            steering *= -1
        left_angle = left_motor.angle()
        right_angle = right_motor.angle()
        while (not abs(left_angle - left_motor.angle()) > degrees
                    or abs(right_angle - right_motor.angle()) > degrees):
            self.steering(power,steering)
        self.stop(stop_type)

    def steering_for_rotations(self,power,steering,rotations,stop_type = "hold"):
        '''左右2つのモーターのどちらかの回転数の変化量が指定した回転数を超えるまでステアリングで走る'''
        self.steering_for_degrees(power,steering,rotations * 360,stop_type)

    # stop-----------------------------------------------------------------------------------------
    def stop(self,stop_type):
        '''Just stop with the specified way'''
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

    def turn_left(self,power,stop_type="hold"):
        self.stop(stop_type)

    def turn_right(self,power,stop_type="hold"):
        self.stop(stop_type)

tank = Tank()
# main program
# 以下Mapの上向きを北として表記する。

if __name__ == '__main__':
    # 1.スタートする
    tank.steering_for_degrees(30,-100,None,"hold")
    while True:
        if color1.color() == "Color.BLACK" and color2.color() == "Color.BLACK":
            break
        tank.drive_pid(30)
    tank.drive_pid_for_degrees(30, None)
    tank.turn_right(30)
    tank.drive_pid_for_degrees(30, None)
    tank.turn_left(30)
    # 2.水をとるx2
    # 3.マーキングブロックを読み取る
    # 　（緑の場合）
    # 　Ⅰ.入口に水を置く
    # 　Ⅱ.ボールをボール入れ
    # 　（白の場合）
    # 　Ⅰ.水を机の上に置くx1
    # 4.洗濯物を回収し、ラインの中央に置く
    # 5. 3,4を向かい側で繰り返す
    # 6.洗濯物x2を回収する
    # 7.洗濯物を洗濯機に入れる。
    # （洗濯機の色と洗濯物のが一致しないと減点）
    # ※洗濯機が枠の外へ動く　GAMEOVER　
    # 8.スタート地点に戻る→終了
