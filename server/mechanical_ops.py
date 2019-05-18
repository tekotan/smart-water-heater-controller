import gpiozero as gz
import time

my_servo = gz.Servo(16)
my_servo.value = None


def update(seconds):
    if seconds > 0:
        my_servo.value = 0.2
        time.sleep(seconds)
        my_servo.value = None
    else:
        my_servo.value = -0.9
        time.sleep(abs(seconds))
        my_servo.value = None
