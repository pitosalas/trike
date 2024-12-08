from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Buzzer, Servo, Motor
import constants
import RPi.GPIO as GPIO
import time

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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(constants.ECHO_PIN,GPIO.IN)
        GPIO.setup(constants.TRIG_PIN,GPIO.OUT)


    def reset(self):
        GPIO.cleanup()

    def start_drive(self, dir: bool, pwm: float):
        if dir:
            self.left.forward(pwm)
            self.right.forward(pwm)
        else:
            self.left.backward(pwm)
            self.right.backward(pwm)
    
    def start_differential_drive(self, linear: float, rotation: float):
        fwd = linear > 0
        linear = abs(linear)
        left_pwm = 0.4
        right_pwm = 0.4
        if rotation < 0:
            left_pwm -= 0.2
        elif rotation > 0:
            right_pwm -= 0.2
        if fwd:
            self.left.forward(left_pwm)
            self.right.forward(right_pwm)
        else:
            self.left.backward(left_pwm)
            self.right.backward(right_pwm)
                                 
    def stop_drive(self): 
        self.left.stop()
        self.right.stop()

    def raw_steer(self, pwm: float):
        self.servo.value = pwm

    def buzzer_on(self):
        self.buzzer.on()

    def raw_buzzer_off(self):
        self.buzzer.off()

    def distance(self):
        GPIO.output(constants.TRIG_PIN,GPIO.LOW)
        time.sleep(0.000001)  # One micro second
        GPIO.output(constants.TRIG_PIN,GPIO.HIGH)
        time.sleep(0.000001)  # One micro second
        GPIO.output(constants.TRIG_PIN,GPIO.LOW)
        start_waiting_for_echo = time.time()
        while not GPIO.input(constants.ECHO_PIN):
            waiting_for_echo = time.time()
            if (waiting_for_echo - start_waiting_for_echo) > 0.03 :
                return -11 # time-out

        echo_start = time.time()
        while GPIO.input(constants.ECHO_PIN):
            waiting_for_echo_end = time.time()
            if(waiting_for_echo_end - echo_start) > 0.05 :
                return -12 # time out

        echo_end = time.time()
        echo_duration = echo_end - echo_start
        time.sleep(0.01)
        return echo_duration * 17150  # Speed of sound * time / 2