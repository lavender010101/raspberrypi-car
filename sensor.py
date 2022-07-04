import RPi.GPIO as GPIO


class Sensor:

    def __init__(self, IR_L, IR_R, IR_F_1, IR_F_2, IR_F_3):
        self.IR_L = IR_L
        self.IR_R = IR_R
        self.IR_F_1 = IR_F_1
        self.IR_F_2 = IR_F_2
        self.IR_F_3 = IR_F_3

        GPIO.setup(IR_L, GPIO.IN)
        GPIO.setup(IR_R, GPIO.IN)
        GPIO.setup(IR_F_1, GPIO.IN)
        GPIO.setup(IR_F_2, GPIO.IN)
        GPIO.setup(IR_F_3, GPIO.IN)

    def check_front(self):
        if GPIO.input(self.IR_F_1) == GPIO.LOW:
            print("--------------- 1 --------------")
        if GPIO.input(self.IR_F_2) == GPIO.LOW:
            print("--------------- 2 --------------")
        if GPIO.input(self.IR_F_3) == GPIO.LOW:
            print("--------------- 3 --------------")
        pass
