import gpiozero as gz
import time

my_servo = gz.Servo(26)
my_servo.value = None


def update(seconds):
    my_servo.value = 0.1
    time.sleep(seconds)
    my_servo.value = None
