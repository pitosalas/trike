from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Buzzer, Servo, Motor
from time import sleep
import constants
import asyncio



class Trike:
    def __init__(self):
        self.fact = PiGPIOFactory()
        self.buzzer = Buzzer(
            constants.BUZZER_PIN, active_high=False, pin_factory=self.fact
        )
        self.servo = Servo(
            constants.SERVO_PIN,
            pin_factory=self.fact,
            min_pulse_width=0.5 / 1000,  # 0.5ms
            max_pulse_width=2.5 / 1000,  # 2.5ms
        )
        self.left = Motor(
            forward=constants.LEFT_FWD,
            backward=constants.LEFT_BACK,
            enable=constants.LEFT_PWM,
            pin_factory=self.fact,
        )
        self.right = Motor(
            forward=constants.RIGHT_FWD,
            backward=constants.RIGHT_BACK,
            enable=constants.RIGHT_PWM,
            pin_factory=self.fact,
        )

    def reset(self):
        pass

    def raw_drive(self, dir: bool, pwm: float):
        self.start_drive(dir, pwm)
        sleep(1)
        self.stop_drive(dir, pwm)

    def raw_start_drive(self, dir: bool, pwm: float):
        if dir:
            self.left.forward(pwm)
            self.right.forward(pwm)
        else:
            self.left.backward(pwm)
            self.right.backward(pwm)
    
    def raw_stop_drive(self, dir, pwm): 
        self.left.stop()
        self.right.stop()

    def raw_steer(self, pwm: float):
        self.servo.value = pwm

    def raw_beep(self, time: float):
        self.buzzer.on()
        sleep(time)
        self.buzzer.off()

    async def beep_every_second(self, duration):
        end_time = asyncio.get_event_loop().time() + duration
        while asyncio.get_event_loop().time() < end_time:
            self.buzzer.on()
            await asyncio.sleep(0.1)  # Short beep
            self.buzzer.off()
            await asyncio.sleep(0.9)  # Wait for remainder of second

    async def move_forward(self, speed, duration):
        self.raw_start_drive(True, speed)
        await asyncio.sleep(duration)
        self.raw_stop_drive.stop()

    async def constant_beep(self, buzzer, duration):
        self.buzzer.play('A4')
        await asyncio.sleep(duration)
        buzzer.stop()

async def main(t: Trike):
    # First section: concurrent beeping and moving
    await asyncio.gather(
        t.beep_every_second(5),
        t.move_forward(0.5, 5)
    )

    # Second section: just beeping
    await t.constant_beep(buzzer, 5)

if __name__ == "__main__":
    t = Trike()
    asyncio.run(main(t))

