import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.board)
PIR_PIN = 26
PIR_INPUT = 19
GPIO.setup(PIR_INPUT, GPIO.OUT)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.output(PIR_INPUT, GPIO.HIGH)
print("initializing sensor")
time.sleep(2)
print("active")


def get_data():
    return GPIO.input(PIR_PIN)


def cleanup():
    GPIO.cleanup()
    print("Cleaned Up Everything")
