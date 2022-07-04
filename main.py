import RPi.GPIO as GPIO
import Vehicle


# wheels settings


# sensor settings


def global_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    pass


if __name__ == '__main__':
    global_setup()
    car = Vehicle()
    try:
        while True:
            car.forward(20)
    except KeyboardInterrupt:
        print("exit by keyboard interrupt")
    finally:
        GPIO.cleanup()
