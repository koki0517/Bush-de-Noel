#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Direction, Color, Button
from pybricks.tools import wait, StopWatch

watch = StopWatch()

color1 = ColorSensor(Port.S1)
color2 = ColorSensor(Port.S2)
color_detect = ColorSensor(Port.S3)

left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

def speed_precent(percentage):
    ''' percentageをdeg/sに変換'''
    return 990 * percentage / 100

class Tank:
    '''PID制御とMovetank,Movesteeringをまとめたclass'''
    Kp = 1.2
    Ki = 0.5
    Kd = 1.0
    individual_difference = 0 #cs2-cs3
    errors = [0,0,0,0,0]

    def drive_pid(self, base_speed):
        error = color1.refrection() - color2.refrection() - Tank.individual_difference
        Tank.errors.append(error)
        del Tank.errors[0]
        control_amount = (Tank.Kp * error
                             + Tank.Ki * sum(Tank.errors)
                                 + Tank.Kd * (error - Tank.errors[-1]))
        left_motor.run(base_speed + control_amount)
        right_motor.run(base_speed - control_amount)

    def drive_pid_for_seconds(self, base_speed, time):
        time_run = watch.time() + time
        while watch.time() <= time_run:
            self.drive_pid(base_speed)

    def drive_pid_for_degrees(self, base_speed):
        pass

    def drive_pid_for_rotations(self, base_speed):
        pass

    def drive(self, left_speed, right_speed):
        '''just drive such as tank'''
        left_motor.run(left_speed)
        right_motor.run(right_speed)

    def drive_for_seconds(self, left_speed, right_speed, time, stop_type = "hold", ifwait=True):
        left_motor.run_time(left_speed, time, stop_type, ifwait)
        left_motor.run_time(right_speed, time, stop_type, ifwait)

    def drive_for_degrees(self, left_speed, right_speed, degrees):
        left_angle = left_motor.angle()
        right_angle = right_motor.angle()
        while not abs(left_angle - left_motor.angle()) > degrees or abs(right_angle - right_motor.angle()) > degrees:
            left_motor.run(left_speed)
            right_motor.run(right_speed)

    def drive_for_rotations(self, left_speed, right_speed, rotations):
        degrees = rotations * 360
        left_angle = left_motor.angle()
        right_angle = right_motor.angle()
        while not abs(left_angle - left_motor.angle()) > degrees or abs(right_angle - right_motor.angle()) > degrees:
            left_motor.run(left_speed)
            right_motor.run(right_speed)

    def steering(self,power,steering):
        '''run on steering forever'''
        if -100 > power or 100 > power:
            raise ValueError
        if -100 <= steering < 0:
            left_motor.run(speed_precent((power / 50) * steering + power)) # 式①
            right_motor.run(speed_precent(power)) # 式②
        elif 0 <= steering <= 100:
            left_motor.run(speed_precent(power)) # 式③
            right_motor.run(speed_precent(-1 * (power / 50) * steering + power)) # 式④
        else:
            raise ValueError

    def steering_for_seconds(self,power,steering,seconds,stop_type = "hold"):
        '''指定された時間ステアリングで走る'''
        if seconds <= 0:
            raise ValueError
        time_run = watch.time() + seconds
        while watch.time() <= time_run:
            self.steering(power,steering)
        self.stop(stop_type)

    def steeing_for_degrees(self,power,steering,degrees,stop_type = "hold"):
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
        self.steeing_for_degrees(power,steering,rotations * 360)
        self.stop(stop_type)

    def stop(self,stop_type):
        '''Just stop'''
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
