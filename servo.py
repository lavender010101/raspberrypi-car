import RPi.GPIO as GPIO


class Servo:

    def __init__(self, channel) -> None:
        self.channel = channel

    def set_angle(self, pwm, angle):
        date = 4096 * (angle * 11 + 500) / 20000
        pwm.set_pwm(self.channel, 0, date)
