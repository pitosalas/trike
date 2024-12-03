from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from time import sleep

factory = PiGPIOFactory()

# Try with explicit BCM notation
echo = DigitalInputDevice("BCM31", pin_factory=factory)
trigger = DigitalOutputDevice("BCM30", pin_factory=factory)

# Alternative pins to test
# echo = DigitalInputDevice("BCM1", pin_factory=factory)
# trigger = DigitalOutputDevice("BCM0", pin_factory=factory)

while True:
    trigger.on()
    sleep(1)
    trigger.off()
    sleep(1)
    print("Echo state:", echo.value)