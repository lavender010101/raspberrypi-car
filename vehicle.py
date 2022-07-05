import RPi.GPIO as GPIO
import time


class Vehicle:

    def __init__(self, pwmA, AIN1, AIN2, pwmB, BIN1, BIN2):
        GPIO.setup(pwmA, GPIO.OUT)
        GPIO.setup(AIN1, GPIO.OUT)
        GPIO.setup(AIN2, GPIO.OUT)

        GPIO.setup(pwmB, GPIO.OUT)
        GPIO.setup(BIN1, GPIO.OUT)
        GPIO.setup(BIN2, GPIO.OUT)

        self.AIN1 = AIN1
        self.AIN2 = AIN2
        self.L_Motor = GPIO.PWM(pwmA, 100)
        self.L_Motor.start(0)

        self.BIN1 = BIN1
        self.BIN2 = BIN2
        self.R_Motor = GPIO.PWM(pwmB, 100)
        self.R_Motor.start(0)

    def forward(self, speed, interval):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN1, True)  # AIN1
        GPIO.output(self.AIN2, False)  # AIN2

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN1, True)  # BIN1
        GPIO.output(self.BIN2, False)  # BIN2

        time.sleep(interval)
        return 'forward'

    def backward(self, speed, interval):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN1, False)  # AIN1
        GPIO.output(self.AIN2, True)  # AIN2

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN1, False)  # BIN1
        GPIO.output(self.BIN2, True)  # BIN2

        time.sleep(interval)
        return 'backward'

    def turn_left(self, speed, interval):
        # backward
        # self.L_Motor.ChangeDutyCycle(speed)
        self.L_Motor.ChangeDutyCycle(0)
        GPIO.output(self.AIN1, False)  #AIN1
        GPIO.output(self.AIN2, True)  #AIN2

        # forward
        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN1, True)  #BIN1
        GPIO.output(self.BIN2, False)  #BIN2
        time.sleep(interval)
        return 'turn_left'

    def turn_right(self, speed, interval):
        # forward
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN1, True)  #AIN1
        GPIO.output(self.AIN2, False)  #AIN2

        # backward
        # self.R_Motor.ChangeDutyCycle(speed)
        self.R_Motor.ChangeDutyCycle(0)
        GPIO.output(self.BIN1, False)  #BIN1
        GPIO.output(self.BIN2, True)  #BIN2
        time.sleep(interval)
        return 'turn_right'

    def stop(self, interval):
        self.L_Motor.ChangeDutyCycle(0)
        GPIO.output(self.AIN1, False)  # AIN1
        GPIO.output(self.AIN2, False)  # AIN2

        self.R_Motor.ChangeDutyCycle(0)
        GPIO.output(self.BIN1, False)  # BIN1
        GPIO.output(self.BIN2, False)  # BIN2

        time.sleep(interval)
        return 'stop'

    def status(self):
        pass
