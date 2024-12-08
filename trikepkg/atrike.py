import asyncio
from hardware import Hardware


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
        self.hardware.start_drive(True, speed)
        await asyncio.sleep(duration)
        self.hardware.stop_drive()

    async def constant_beep(self, duration):
        self.hardware.buzzer.on()
        await asyncio.sleep(duration)
        self.hardware.buzzer.off()
    
    async def diff_drive(self, lin: float, ang: float, dur: float):
        self.hardware.start_differential_drive(linear=lin, angular=ang)
        await asyncio.sleep(dur)
        self.hardware.stop_drive()
       
    async def set_steering(self, pwm):
        self.hardware.servo.value = pwm

    async def poll_distance(self):
        try:
            while True:
                self.distance = self.hardware.distance()
                await asyncio.sleep(0.1)                        # Add a small delay to prevent CPU overload
        except asyncio.CancelledError:
            # Handle clean shutdown when the task is cancelled
            pass

