import RPi.GPIO as GPIO
# from Vehicle import *

pwmA = 12
AIN1 = 15
AIN2 = 13

pwmB = 16
BIN1 = 22
BIN2 = 18
# sensor settings


class Vehicle(object):

    def __int__(self, pwmA, AIN1, AIN2, pwmB, BIN1, BIN2):
        GPIO.setup(pwmA, GPIO.OUT)
        GPIO.setup(AIN1, GPIO.OUT)
        GPIO.setup(AIN2, GPIO.OUT)

        GPIO.setup(pwmB, GPIO.OUT)
        GPIO.setup(BIN1, GPIO.OUT)
        GPIO.setup(BIN2, GPIO.OUT)

        self.AIN1 = AIN1
        self.AIN2 = AIN2
        self.L_Motor = GPIO.PWM(pwmA)
        self.L_Motor.start(0)

        self.BIN1 = BIN1
        self.BIN2 = BIN2
        self.R_Motor = GPIO.PWM(pwmB)
        self.R_Motor.start(0)

    def forward(self, speed, time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN1, True)  # AIN1
        GPIO.output(self.AIN2, False)  # AIN2

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN1, True)  # BIN1
        GPIO.output(self.BIN2, False)  # BIN2

        time.sleep(time)

    def backward(self, speed, time):
        pass

    def turn_left(self, speed, time):
        pass

    def turn_right(self, speed, time):
        pass

    def stop(self, time):
        self.L_Motor.ChangeDutyCycle(0)
        GPIO.output(self.AIN1, False)  # AIN1
        GPIO.output(self.AIN2, False)  # AIN2

        self.R_Motor.ChangeDutyCycle(0)
        GPIO.output(self.BIN1, False)  # BIN1
        GPIO.output(self.BIN2, False)  # BIN2

        time.sleep(time)


def global_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    pass


if __name__ == '__main__':
    global_setup()
    car = Vehicle()
    # car = Vehicle()
    try:
        while True:
            car.forward(20)
    except KeyboardInterrupt:
        print("exit by keyboard interrupt")
    finally:
        GPIO.cleanup()
