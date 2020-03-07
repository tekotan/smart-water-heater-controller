import gpiozero as gz
import time

#my_servo = gz.Servo(20)
#my_servo.value = None


#def update(seconds):
#    my_servo.value = 0.4
#    time.sleep(abs(seconds))
#    my_servo.value = None
#update(2)
led = gz.LED(20)

def update(seconds):
    led.on()
    time.sleep(seconds)
    led.off()

