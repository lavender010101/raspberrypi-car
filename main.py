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


def global_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    pass


if __name__ == '__main__':
    global_setup()
    # car = Vehicle()
    car = Vehicle(pwmA, AIN1, AIN2, pwmB, BIN1, BIN2)
    # car = Vehicle()
    sensor = Sensor(IR_L, IR_R, IR_F_L, IR_F_R)
    try:
        while True:
            sensor.check_front()
            car.forward(20,0)
            time.sleep(1)

            os.system('clear')

            # car.forward(60, 0)
    except KeyboardInterrupt:
        print("exit by keyboard interrupt")
    finally:
        GPIO.cleanup()
