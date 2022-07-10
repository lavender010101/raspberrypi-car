#!/usr/bin/env python
# coding=UTF-8
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import time
import socket
import sys

# reload(sys)
# sys.setdefaultencoding('utf8')

PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24


# 舵机摇头代码
class CarServo:

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
            self.pwm_pca9685.set_pwm(channel, 0, date)
            self.servo[channel] = new_angle
        else:
            print("set_servo_angle error. servo[{0}] = [{1}]".format(
                channel, angle))

    def inc_servo_angle(self, channel, v):
        self.set_servo_angle(channel, self.servo[channel] + v)

    def dec_servo_angle(self, channel, v):
        self.set_servo_angle(channel, self.servo[channel] - v)


def t_up(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    # up
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1


def t_down(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1


def t_left(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1


def t_right(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1


def t_stop():
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    # stop
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, False)  # BIN1


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)

GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 100)
L_Motor.start(0)

R_Motor = GPIO.PWM(PWMB, 100)
R_Motor.start(0)

cs = CarServo()

# 下面是命令接收代码
ip_port = ('', 7878)  # 留空才能接收来自局域网的UDP连接
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)  # 创建套接字
sk.bind(ip_port)  # 绑定服务地址
print('启动socket服务，等待客户端连接...')
try:
    while True:
        client_data = sk.recv(1024).strip().decode()  # 接收遥控命令,使用字符串分割来接收多个命令参数
        print("客户端向你发来信息：%s" % (client_data))
        order_list = client_data.split(',')  # 将接收到的命令通过逗号分割
        o = int(order_list[0])  # 第一个为小车的运行方向
        speed = int(order_list[1])  # 第二个为小车的运行速度
        iod = int(
            order_list[2])  # 第三个参数为判断increase_channel(0)或decrease_channel(1)
        channel = int(order_list[3])  # 第四个参数为了获得channel的值
        angel = int(order_list[4])  # 第五个参数为获得angel的值
        type = int(order_list[5]
                   )  # 第六个参数用于判断是接受到了马达命令还是舵机命令,0马达,1舵机,这样就不怕马达和舵机命令相互干扰了
        # 马达命令示例:1,50,0,0,0,1 以50的速度前进
        # 舵机命令示例:0,0,0,1,20,2 舵机向左转动20度
        if type == 1:  # 如果收到了马达命令
            if speed == 0:  # 如果没有收到speed参数，或speed为0，则调整为50
                speed = 50
            if o == 0:  # 0停止小车
                t_stop()
            elif o == 1:  # 1前进
                t_up(speed)
            elif o == 2:  # 2后退
                t_down(speed)
            elif o == 3:  # 3左转
                t_left(speed)
            elif o == 4:  # 4右转
                t_right(speed)
        if type == 2:  # 如果收到了舵机命令
            if iod == 0:  # increase_channel:1左2下
                cs.inc_servo_angle(channel, angel)
            elif iod == 1:  # decrease_channel:1右2上
                cs.dec_servo_angle(channel, angel)

finally:
    GPIO.cleanup()
    sk.close()
