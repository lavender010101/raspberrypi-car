import socket, sys, os
import RPi.GPIO as GPIO
from vehicle import *
from sensor import *
# from servo import *
from PCA9685 import PCA9685
from server_app import CarServo

pwmA = 12
AIN1 = 15
AIN2 = 13

pwmB = 16
BIN1 = 22
BIN2 = 18
# sensor settings
IR_L = 32
IR_R = 36
# IR_F_2 = 35
IR_F_L = 37
IR_F_R = 33

US_T = 38
US_R = 40

# button
btn_pin = 35

vertical_angle = 500
orient_angle = 1500

control_mode = 'pc_control'

server_host = '0.0.0.0'
server_port = 2022

speed = 50


def global_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(btn_pin, GPIO.IN)
    global pwm
    pwm = PCA9685(0x40)
    pwm.setPWMFreq(50)

    pwm.setServoPulse(13, orient_angle)
    pwm.setServoPulse(14, vertical_angle)


def servo_control(servo, angle, interval):
    pwm.setServoPulse(servo, angle)
    time.sleep(interval)


def pc_control(action, car, vertical_angle, orient_angle):
    if action == 'forward':
        # print('forward')
        car.forward(speed, 0)
    elif action == 'backward':
        car.backward(speed, 0)
        # print('backward')
    elif action == 'turn_left':
        car.turn_left(speed, 0)
        # print('turn_left')
    elif action == 'turn_right':
        car.turn_right(speed, 0)
        # print('turn_right')
    elif action == 'stop':
        car.stop(0)
        # print('stop')
    elif action == 'servo_up':
        vertical_angle -= 11
        servo_control(14, vertical_angle, 0.008)
        # pwm.setServoPulse(14, vertical_angle)
        # time.sleep(0.008)
    elif action == 'servo_down':
        vertical_angle += 11
        servo_control(14, vertical_angle, 0.008)
        # pwm.setServoPulse(14, vertical_angle)
        # time.sleep(0.008)
    elif action == 'servo_turn_left':
        orient_angle += 11
        servo_control(13, orient_angle, 0.008)
        # pwm.setServoPulse(13, orient_angle)
        # time.sleep(0.008)
    elif action == 'servo_turn_right':
        orient_angle -= 11
        servo_control(13, orient_angle, 0.008)
        # pwm.setServoPulse(13, orient_angle)
        # time.sleep(0.008)
    elif action.isdigit():
        print('change speed')

    return vertical_angle, orient_angle


ip_port = ('', 7878)  # 留空才能接收来自局域网的UDP连接
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)  # 创建套接字
sk.bind(ip_port)  # 绑定服务地址


def app_control(client_data, car, cs):

    # print("客户端向你发来信息：%s" % (client_data))
    order_list = client_data.split(',')  # 将接收到的命令通过逗号分割
    action = int(order_list[0])  # 第一个为小车的运行方向
    speed = int(order_list[1])  # 第二个为小车的运行速度
    iod = int(order_list[2])  # 第三个参数为判断increase_channel(0)或decrease_channel(1)
    channel = int(order_list[3])  # 第四个参数为了获得channel的值
    angel = int(order_list[4])  # 第五个参数为获得angel的值
    type = int(
        order_list[5])  # 第六个参数用于判断是接受到了马达命令还是舵机命令,0马达,1舵机,这样就不怕马达和舵机命令相互干扰了
    # 马达命令示例:1,50,0,0,0,1 以50的速度前进
    # 舵机命令示例:0,0,0,1,20,2 舵机向左转动20度
    if type == 1:  # 如果收到了马达命令
        if speed == 0:  # 如果没有收到speed参数，或speed为0，则调整为50
            speed = 50
        if action == 0:  # 0停止小车
            car.stop(0)
        elif action == 1:  # 1前进
            car.backward(speed, 0)
        elif action == 2:  # 2后退
            car.backward(speed, 0)
        elif action == 3:  # 3左转
            car.turn_left(speed, 0)
        elif action == 4:  # 4右转
            car.turn_right(speed, 0)
    if type == 2:  # 如果收到了舵机命令
        if iod == 0:  # increase_channel:1左2下
            cs.inc_servo_angle(channel, angel)
        elif iod == 1:  # decrease_channel:1右2上
            cs.dec_servo_angle(channel, angel)


if __name__ == '__main__':
    global_setup()
    car = Vehicle(pwmA, AIN1, AIN2, pwmB, BIN1, BIN2)
    sensor = Sensor(IR_L, IR_R, IR_F_L, IR_F_R, US_T, US_R)
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_host, server_port))
        server_socket.listen()

        client_socket, address = server_socket.accept()
        cs = CarServo()

        while True:
            if control_mode == 'pc_control':
                action = client_socket.recv(1024).decode('utf-8')

                if action == 'exit':
                    break
                vertical_angle, orient_angle = pc_control(
                    action, car, vertical_angle, orient_angle)
            elif control_mode == 'app_control':
                client_data = sk.recv(
                    1024).strip().decode()  # 接收遥控命令,使用字符串分割来接收多个命令参数

                app_control(client_data, car, cs)

    except KeyboardInterrupt:
        print("exit by keyboard interrupt")
    finally:
        GPIO.cleanup()
