from gpiozero.pins.rpigpio import RPiGPIOFactory
from gpiozero import Buzzer
from gpiozero import Servo
from time import sleep
from trike.constants import *

class Trike:
    def __init__(self):
        self.fact = RPiGPIOFactory()

    def reset(self):
        pass

    def raw_drive(self, pwm: float, time: float):
        pass

    def raw_steer(self, pwm: float):
        servo = Servo(SERVO_PIN,)
        servo.value = pwm

    def raw_beep(self, time: float):
        buzzer = Buzzer(BUZZER_PIN, active_high=False, pin_factory=self.fact)
        buzzer.on()
        sleep(time)
        buzzer.off()

if __name__ == "__main__":
    t = Trike()
    t.raw_beep(3)
    t.raw_servo()