import RPi.GPIO as GPIO


class Sensor:

    def __init__(self, IR_L, IR_R, IR_F_L, IR_F_R, US_T, US_R):
        #
        self.IR_L = IR_L
        self.IR_R = IR_R
        GPIO.setup(IR_L, GPIO.IN)
        GPIO.setup(IR_R, GPIO.IN)

        #
        self.IR_F_L = IR_F_L
        # self.IR_F_2 = IR_F_2
        self.IR_F_R = IR_F_R
        GPIO.setup(IR_F_R, GPIO.IN)
        # GPIO.setup(IR_F_2, GPIO.IN)
        GPIO.setup(IR_F_L, GPIO.IN)

        # ultrasonic
        self.US_T = US_T
        self.US_R = US_R
        GPIO.setup(US_T, GPIO.OUT)
        GPIO.setup(US_R, GPIO.IN)
        GPIO.output(US_T, True)

    # 寻迹
    def trace_trail(self):
        # 哪个方向灯亮了
        left = GPIO.input(self.IR_F_L) == GPIO.LOW
        right = GPIO.input(self.IR_F_R) == GPIO.LOW
        if left and right:
            return 'forward'
        elif left and not right:
            return 'turn_right'
        elif not left and right:
            return 'turn_left'
        elif not left and not right:
            return 'stop'

    # 避障碍
    def avoid_obstacles(self):

        front = GPIO.input(self.US_R) == GPIO.LOW
        left = GPIO.input(self.IR_F_L) == GPIO.HIGH
        right = GPIO.input(self.IR_F_R) == GPIO.HIGH
        if left and not right:
            return 'turn_left'
        elif not left and right:
            return 'turn_right'
        if front:
            return 'forward'
        else:
            return 'backward'
        pass
