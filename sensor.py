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
        left = GPIO.input(self.IR_F_L) == GPIO.LOW
        right = GPIO.input(self.IR_F_R) == GPIO.LOW
        if left and right:
            return 'forward'
        elif left and not right:
            return 'turn_left'
        elif not left and right:
            return 'turn_right'
        elif not left and not right:
            return 'stop'
        # pass
