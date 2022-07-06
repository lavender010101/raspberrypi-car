import RPi.GPIO as GPIO
import time


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
    def distance_measure(self):
        GPIO.output(self.US_T, False)
        time.sleep(0.000002)
        GPIO.output(self.US_T, True)
        time.sleep(0.00001)
        GPIO.output(self.US_T, False)

        miss_target_time = 0
        while GPIO.input(self.US_R) == 0:
            miss_target_time += 1
            if miss_target_time > 10000:
                print('Missing the echo')
                return 0

        start_time = time.time()

        while GPIO.input(self.US_R) == 1:
            pass

        time_span = time.time() - start_time

        # distance = time_span * 340m / 2
        return time_span * 17150

    def avoid_obstacles(self):
        # GPIO.output(self.US_T, True)
        # front = GPIO.input(self.US_R) == GPIO.LOW
        distance = self.distance_measure()
        left = GPIO.input(self.IR_L) == GPIO.HIGH
        right = GPIO.input(self.IR_R) == GPIO.HIGH
        if left and not right:
            return 'turn_left'
        elif not left and right:
            return 'turn_right'
        elif not left and not right:
            if distance < 10:
                return 'stop'

        # front distance (cm)
        # print("%.2f cm" % distance)

        if distance < 5:
            return 'backward'
        elif distance > 15:
            return 'forward'
        else:
            return 'slow_forward'
