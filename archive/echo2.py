from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
from time import sleep
import RPi.GPIO as GPIO
ECHO_PIN = 30
TRIG_PIN = 31

# factory = LGPIOFactory()
factory = PiGPIOFactory()
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(ECHO_PIN,GPIO.IN)
# GPIO.setup(TRIG_PIN,GPIO.OUT)

sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, pin_factory=factory)
while True:
    print("Distance: ", sensor.distance * 100)
    sleep(1)
