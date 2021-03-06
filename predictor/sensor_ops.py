import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIR_PIN = 21
def setup():

    GPIO.setup(PIR_PIN, GPIO.IN)

    print("initializing sensor")
    time.sleep(2)
    print("active")


def get_data():
    return GPIO.input(PIR_PIN)


def cleanup():
    GPIO.cleanup()
    print("Cleaned Up Everything")
