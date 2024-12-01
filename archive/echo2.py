from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
from time import sleep

fact = PiGPIOFactory()
sensor = DistanceSensor(echo="GPIO0", trigger="GPIO1", pin_factory=fact)

while True:
    print('Distance: ', sensor.distance * 100)
    sleep(1)
