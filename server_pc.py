import socket, sys, os
import RPi.GPIO as GPIO
from vehicle import *
from sensor import *
# from servo import *
from PCA9685 import PCA9685

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
    global pwm
    # pwm = Adafruit_PCA9685.PCA9685()
    # pwm.set_pwm_freq(50)
    pwm = PCA9685(0x40)
    pwm.setPWMFreq(50)

    pwm.setServoPulse(13, orient_angle)
    pwm.setServoPulse(14, vertical_angle)


def servo_control(servo, angle, interval):
    pwm.setServoPulse(servo, angle)
    time.sleep(interval)


if __name__ == '__main__':
    global_setup()
    car = Vehicle(pwmA, AIN1, AIN2, pwmB, BIN1, BIN2)
    sensor = Sensor(IR_L, IR_R, IR_F_L, IR_F_R, US_T, US_R)
    try:
        server_host = '0.0.0.0'
        server_port = 2022
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_host, server_port))
        server_socket.listen()

        client_socket, address = server_socket.accept()

        while True:
            action = client_socket.recv(1024).decode('utf-8')
            # print(action)

            if action == 'forward':
                print('forward')
            elif action == 'backward':
                print('backward')
            elif action == 'turn_left':
                print('turn_left')
            elif action == 'turn_right':
                print('turn_right')
            elif action == 'stop':
                print('stop')
            elif action == 'servo_up':
                vertical_angle -= 5
                pwm.setServoPulse(14, vertical_angle)
                time.sleep(0.008)
                # print('servo_up')
            elif action == 'servo_down':
                vertical_angle += 5
                pwm.setServoPulse(14, vertical_angle)
                time.sleep(0.008)
                # print('servo_down')
            elif action == 'servo_turn_left':
                orient_angle += 5
                pwm.setServoPulse(13, orient_angle)
                time.sleep(0.008)
                # print('servo_turn_left')
            elif action == 'servo_turn_right':
                orient_angle -= 5
                pwm.setServoPulse(13, orient_angle)
                time.sleep(0.008)
                # print('servo_turn_right')
            elif action.isdigit():
                # speed = eval(action)
                print('change speed')
            elif action == 'exit':
                break

        pass
    except KeyboardInterrupt:
        print("exit by keyboard interrupt")
    finally:
        GPIO.cleanup()
