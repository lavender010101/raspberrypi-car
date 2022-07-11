import socket, sys, os
import RPi.GPIO as GPIO
from vehicle import *
from sensor import *
# from servo import *
# from PCA9685 import PCA9685
from servo import Servo
import threading

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


def global_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(btn_pin, GPIO.IN)
    # global pwm
    # pwm = Adafruit_PCA9685.PCA9685()
    # pwm.set_pwm_freq(50)
    # pwm = PCA9685(0x40)
    # pwm.setPWMFreq(50)
    #
    # pwm.setServoPulse(13, orient_angle)
    # pwm.setServoPulse(14, vertical_angle)


def car_handler(car, servo, client_socket):
    # 接收遥控命令,使用字符串分割来接收多个命令参数
    order = client_socket.recv(1024).strip().decode().split(',')
    device = order[0]
    action = order[1]
    print('device = ' + device)
    print('action = ' + action)
    if device == 'car':
        speed = int(order[2])
        if action == 'forward':
            car.forward(speed, 0)
        elif action == 'backward':
            car.backward(speed, 0)
        elif action == 'turn_left':
            car.turn_left(speed, 0)
        elif action == 'turn_right':
            car.turn_right(speed, 0)
        elif action == 'stop':
            car.stop(0)
    elif device == 'servo':
        angle = int(order[2])
        if action == 'up':
            servo.desc_servo_angle(2, angle)
        elif action == 'down':
            servo.asc_servo_angle(2, angle)
        elif action == 'left':
            servo.asc_servo_angle(1, angle)
        elif action == 'right':
            servo.desc_servo_angle(1, angle)


if __name__ == "__main__":
    print('启动socket服务，等待客户端连接...')
    global_setup()
    car = Vehicle(pwmA, AIN1, AIN2, pwmB, BIN1, BIN2)
    servo = Servo()
    sensor = Sensor(IR_L, IR_R, IR_F_L, IR_F_R, US_T, US_R)

    # socket
    ip_port = ('0.0.0.0', 7878)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建套接字
    server_socket.bind(ip_port)  # 绑定服务地址
    server_socket.listen(10)

    try:

        while True:
            client_socket, _ = server_socket.accept()
            # order = order
            # print(order)
            # car_handler(car, servo, order)
            thread = threading.Thread(target=car_handler,
                                      args=(car, servo, client_socket))
            thread.setDaemon(True)
            thread.start()

    finally:
        GPIO.cleanup()
        server_socket.close()
        # client_socket.close()
