import RPi.GPIO as GPIO


class Sensor:

    def __init__(self, IR_L, IR_R, IR_F_L, IR_F_R):
        self.IR_L = IR_L
        self.IR_R = IR_R
        self.IR_F_L = IR_F_L
        # self.IR_F_2 = IR_F_2
        self.IR_F_R = IR_F_R

        GPIO.setup(IR_L, GPIO.IN)
        GPIO.setup(IR_R, GPIO.IN)
        GPIO.setup(IR_F_R, GPIO.IN)
        # GPIO.setup(IR_F_2, GPIO.IN)
        GPIO.setup(IR_F_L, GPIO.IN)

    def check_front(self):
        if GPIO.input(self.IR_F_L) == GPIO.LOW:
            print("--------------- turn right --------------")
        # if GPIO.input(self.IR_F_2) == GPIO.LOW:
        #     print("--------------- 2 --------------")
        if GPIO.input(self.IR_F_R) == GPIO.LOW:
            print("--------------- turn left --------------")
        # pass
