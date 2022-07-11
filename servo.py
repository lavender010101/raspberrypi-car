import Adafruit_PCA9685


# 舵机摇头代码
class Servo:

    def __init__(self):
        # 2个摄像头舵机,1个超声波舵机
        self.pwm_pca9685 = Adafruit_PCA9685.PCA9685()
        self.pwm_pca9685.set_pwm_freq(50)

        self.servo = {}

        self.set_servo_angle(0, 110)
        self.set_servo_angle(1, 100)
        self.set_servo_angle(2, 20)

    # 输入角度转换成12^精度的数值
    def set_servo_angle(self, channel, angle):
        if (channel >= 0) and (channel <= 2):
            new_angle = angle
            if angle < 0:
                new_angle = 0
            elif angle > 180:
                new_angle = 180
            else:
                new_angle = angle
            print("channel={0}, angle={1}".format(channel, new_angle))
            # date=4096*((new_angle*11)+500)/20000#进行四舍五入运算 date=int(4096*((angle*11)+500)/(20000)+0.5)
            date = int(4096 * ((new_angle * 11) + 500) / (20000) + 0.5)
            self.pwm_pca9685.set_pwm(channel + 12, 0, date)
            self.servo[channel] = new_angle
        else:
            print("set_servo_angle error. servo[{0}] = [{1}]".format(
                channel, angle))

    def asc_servo_angle(self, channel, v):
        self.set_servo_angle(channel, self.servo[channel] + v)

    def desc_servo_angle(self, channel, v):
        self.set_servo_angle(channel, self.servo[channel] - v)
