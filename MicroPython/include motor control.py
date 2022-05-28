#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Direction, Color, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

left_motor.reset_angle(0)
right_motor.reset_angle(0)

color_left = ColorSensor(Port.S1)
color_right = ColorSensor(Port.S2)

watch = StopWatch()

class Tank:
    Kp = 1.2
    Ki = 0.5
    Kd = 1.0
    individual_difference = 0 #cs2-cs3
    errors = [0,0,0,0,0]

    def drive_pid(self, base_speed):
        error = color2.refrection() - color3.refrection() - Tank.individual_difference
        Tank.errors.append(error)
        del Tank.errors[0]
        u = Tank.Kp * error + Tank.Ki * sum(Tank.errors) + Tank.Kd * (error - Tank.errors[-1])
        left_motor.run(base_speed + u)
        right_motor.run(base_speed - u)
    
    def drive_pid_for_seconds(self, base_speed, time, stop_type = "hold"):
        time_run = watch.time() 
        while watch.time() <= time_run:
            self.drive_pid()
        
        self.stop(stop_type)
    
    def drive_pid_for_degrees(self, base_speed, degrees, stop_type = "hold"):
        left_angle = left_motor.angle()
        right_angle = right_motor.angle()
        while not abs(left_angle - left_motor.angle()) > degrees or abs(right_angle - right_motor.angle()) > degrees:
            self.drive_pid()
        
        self.stop(stop_type)
    
    def drive_pid_for_rotations(self, base_speed, rotations, stop_type = "hold"):
        degrees = rotations * 360
        left_angle = left_motor.angle()
        right_angle = right_motor.angle()
        while not abs(left_angle - left_motor.angle()) > degrees or abs(right_angle - right_motor.angle()) > degrees:
            self.drive_pid()
        
        self.stop(stop_type)
    
    def drive(self, left_speed, right_speed):
        left_motor.run(left_speed)
        right_motor.run(right_speed)

    def drive_for_seconds(self, left_speed, right_speed, time, stop_type = "hold", wait=True):
        left_motor.run_time(left_speed, time, stop_type, False)
        left_motor.run_time(left_speed, time, stop_type, False)
        if wait:
            wait(time)
        
        self.stop(stop_type)

    def drive_for_degrees(self, left_speed, right_speed, degrees, stop_type = "hold"):
        left_angle = left_motor.angle()
        right_angle = right_motor.angle()
        while not abs(left_angle - left_motor.angle()) > degrees or abs(right_angle - right_motor.angle()) > degrees:
            left_motor.run(left_speed)
            right_motor.run(right_speed)
        
        self.stop(stop_type)
    
    def drive_for_rotations(self, left_speed, right_speed, rotations, stop_type = "hold"):
        degrees = rotations * 360
        left_angle = left_motor.angle()
        right_angle = right_motor.angle()
        while not abs(left_angle - left_motor.angle()) > degrees or abs(right_angle - right_motor.angle()) > degrees:
            left_motor.run(left_speed)
            right_motor.run(right_speed)
        
        self.stop(stop_type)
    
    def drive_steering(self, base_speed, steering, stop_type = "hold", wait=True):
        left_motor.run(left_speed)
        right_motor.run(right_speed)

    def drive_steering_for_seconds(self, base_speed, steering, time, stop_type = "hold", wait=True):
        pass
    
    def drive_steering_for_degrees(self, base_speed, steering, degrees, stop_type = "hold", wait=True):
        pass

    def drive_steering_for_rotations(self, base_speed, steering, rotations, stop_type = "hold", wait=True):
        pass

    def stop(self, stop_type):
        if stop_type == "stop":
            left_motor.stop()
            right_motor.stop()
        elif stop_type == "brake":
            left_motor.brake()
            right_motor.brake()
        else:
            left_motor.hold()
            right_motor.hold()