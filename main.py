import RPi.GPIO as GPIO
from vehicle import *

pwmA = 12
AIN1 = 15
AIN2 = 13

pwmB = 16
BIN1 = 22
BIN2 = 18
# sensor settings


def global_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    pass


if __name__ == '__main__':
    global_setup()
    # car = Vehicle()
    car = Vehicle(pwmA, AIN1, AIN2, pwmB, BIN1, BIN2)
    # car = Vehicle()
    try:
        while True:
            # car.forward(40, 0)
            # car.backward(100, 0)
            # car.turn_left(40, 0)
            car.turn_right(40, 0)
    except KeyboardInterrupt:
        print("exit by keyboard interrupt")
    finally:
        GPIO.cleanup()
