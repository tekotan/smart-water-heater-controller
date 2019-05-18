import gpiozero as gz
import time

my_servo = gz.Servo(26)
my_servo.value = None


def update(time):
    my_servo.value = 0.1
    time.sleep(time)
    my_servo.value = None
