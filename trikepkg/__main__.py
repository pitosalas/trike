from hardware import Hardware
from atrike import ATrike
import asyncio
import atexit

def cleanup():
    print("Exit")

atexit.register(cleanup)

async def monitor_and_beep(t: ATrike):
    while True:
        if t.distance < 15:
            await t.constant_beep(0.1)
        await asyncio.sleep(0.1)

async def main(t: ATrike):
    # await t.set_steering(constants.SERVO_MID)

    await asyncio.gather(
        t.poll_distance(),
    #    monitor_and_beep(t),
    #     # t.beep_every_second(5),
    #     # t.move_forward(0.15, 5)
    #    t.diff_drive(lin=0.1, ang=-0.1, dur=1)
    )

    # # await t.set_steering(constants.SERVO_LEFT)

    # await t.move_forward(0.15, 5)
    
    # await t.constant_beep(1)



if __name__ == "__main__":
    hardware = Hardware()
    trike = ATrike(hardware)
    # while True:
    #     print(f"dist: {hardware.distance()}")
    asyncio.run(main(trike))
    hardware.reset()

