import RPi.GPIO as GPIO


class Sensor:

    def __init__(self, IR_L, IR_R, IR_F_1, IR_F_2, IR_F_3):
        self.IR_L = IR_L
        self.IR_R = IR_R
        self.IR_F_1 = IR_F_1
        self.IR_F_1 = IR_F_2
        self.IR_F_1 = IR_F_3
