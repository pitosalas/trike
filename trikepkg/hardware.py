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