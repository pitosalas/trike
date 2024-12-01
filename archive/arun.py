from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Buzzer, Servo, Motor
import constants


class Hardware:
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

    def raw_start_drive(self, dir: bool, pwm: float):
        if dir:
            self.left.forward(pwm)
            self.right.forward(pwm)
        else:
            self.left.backward(pwm)
            self.right.backward(pwm)
    
    def raw_stop_drive(self): 
        self.left.stop()
        self.right.stop()

    def raw_steer(self, pwm: float):
        self.servo.value = pwm

    def raw_buzzer_on(self):
        self.buzzer.on()

    def raw_buzzer_off(self):
        self.buzzer.off()

class ATrike:
    def __init__(self, h: Hardware):
        self.hardware = h

    async def beep_every_second(self, duration):
        end_time = asyncio.get_event_loop().time() + duration
        while asyncio.get_event_loop().time() < end_time:
            self.hardware.buzzer.on()
            await asyncio.sleep(0.1)  # Short beep
            self.hardware.buzzer.off()
            await asyncio.sleep(0.9)  # Wait for remainder of second

    async def move_forward(self, speed, duration):
        self.hardware.raw_start_drive(True, speed)
        await asyncio.sleep(duration)
        self.hardware.raw_stop_drive()

    async def constant_beep(self, duration):
        self.hardware.buzzer.on()
        await asyncio.sleep(duration)
        self.hardware.buzzer.off()

    async def set_steering(self, pwm):
        self.hardware.servo.value = pwm

    async def main(self):
        # section: center streering
        await self.set_steering(constants.SERVO_MID)

        # section: concurrent beeping and moving
        await asyncio.gather(
            self.beep_every_second(5),
            self.move_forward(0.15, 5)
        )
        # section: just beeping
        await self.constant_beep(1)

        # section turn wheel sharply and slow down
        await self.set_steering(constants.SERVO_LEFT)
        await self.move_forward(0.15, 5)
        
if __name__ == "__main__":
    hardware = Hardware()
    trike = ATrike(hardware)
    asyncio.run(trike.main())

