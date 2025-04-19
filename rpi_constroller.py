import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

def open_door():
    GPIO.output(18, GPIO.HIGH)

open_door()
