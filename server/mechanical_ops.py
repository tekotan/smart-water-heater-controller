import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
SERVO_PIN = 10
GPIO.setup(SERVO_PIN, GPIO.OUT)

time.sleep(2)
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(5)

def update(self, angle):
    #insert calculated linear function for the servo
    duty = float(angle) / 10.0 + 2.5
    pwm.ChangeDutyCycle(duty)