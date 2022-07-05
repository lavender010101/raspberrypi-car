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


def track(direction):

    if sensor.trace_trail() == 'turn_left':
        # car.forward(14, 0)
        car.turn_left(24, 0)
        direction = 'left'

        # if sensor.trace_trail() ==

    if sensor.trace_trail() == 'turn_right':
        # car.forward(14, 0)
        car.turn_right(24, 0)

        direction = 'right'
    if sensor.trace_trail() == 'forward':
        car.forward(28, 0)
        direction = 'forward'

    if sensor.trace_trail() == 'stop':
        # car.stop(0)
        car.forward(10, 0)
        if direction == 'left':
            car.turn_left(24, 0)
        elif direction == 'right':
            car.turn_right(24, 0)
    time.sleep(0.008)

    # os.system('clear')


if __name__ == '__main__':
    global_setup()
    # car = Vehicle()
    car = Vehicle(pwmA, AIN1, AIN2, pwmB, BIN1, BIN2)
    # car = Vehicle()
    sensor = Sensor(IR_L, IR_R, IR_F_L, IR_F_R, US_T, US_R)
    try:
        direction = 'forward'
        while True:
            track(direction)

#            time.sleep(1)
# car.forward(60, 0)
    except KeyboardInterrupt:
        print("exit by keyboard interrupt")
    finally:
        GPIO.cleanup()
