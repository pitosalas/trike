import asyncio
from hardware import Hardware


class ATrike:
    def __init__(self, h: Hardware):
        self.hardware : Hardware = h
        self.distance : float = 0.0

    async def repeat_beep(self, duration):
        end_time = asyncio.get_event_loop().time() + duration
        while asyncio.get_event_loop().time() < end_time:
            self.hardware.buzzer.on()
            await asyncio.sleep(0.05)  # Short beep
            self.hardware.buzzer.off()
            await asyncio.sleep(0.9)  # Wait for remainder of second

    async def beep_distance1(self):
        while True:
            if self.distance < 50:
                self.hardware.buzzer.on()
                await asyncio.sleep(0.1)
                self.hardware.buzzer.off()
                if self.distance < 20:
                    sleep = 0.9
                else:
                    sleep = 2.9
                await asyncio.sleep(sleep) 

    async def log_distance(self):
        while True:
            print(f"Log distance: {self.distance:.2f}")
            await asyncio.sleep(1) 
          

    async def beep_distance(self):
        while True:
            if self.distance < 20:
                await self.repeat_beep(1.0)
            elif self.distance < 50:
                await self.repeat_beep(5.0)
            await asyncio.sleep(0.05)

    async def poll_distance(self):
        try:
            while True:
                self.distance = self.hardware.distance()
                await asyncio.sleep(0.1) 
        except asyncio.CancelledError:
            # Handle clean shutdown when the task is cancelled
            pass



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

