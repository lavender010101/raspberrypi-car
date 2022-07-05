import RPi.GPIO as GPIO
from vehicle import *
from sensor import *
import os

pwmA = 12
AIN1 = 15
AIN2 = 13

pwmB = 16
BIN1 = 22
BIN2 = 18
# sensor settings
IR_L = 32
IR_R = 36
# IR_F_2 = 35
IR_F_L = 37
IR_F_R = 33

US_T = 38
US_R = 40


def global_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    pass


def track(speed):

    if sensor.trace_trail() == 'turn_left':
        car.turn_left(speed * 1.2, 0)
    elif sensor.trace_trail() == 'turn_right':
        car.turn_right(speed * 1.2, 0)
    elif sensor.trace_trail() == 'forward':
        car.forward(speed, 0)
    elif sensor.trace_trail() == 'stop':
        car.forward(speed * 0.8, 0)

    time.sleep(0.008)


def avoid(speed):
    print(sensor.avoid_obstacles())
    time.sleep(1)


if __name__ == '__main__':
    global_setup()
    car = Vehicle(pwmA, AIN1, AIN2, pwmB, BIN1, BIN2)
    sensor = Sensor(IR_L, IR_R, IR_F_L, IR_F_R, US_T, US_R)
    try:
        while True:
            track(20)
            # avoid(10)

    except KeyboardInterrupt:
        print("exit by keyboard interrupt")
    finally:
        GPIO.cleanup()
