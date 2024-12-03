from hardware import Hardware
from atrike import ATrike
import constants
import asyncio
from gpiozero import Device
import atexit

def cleanup():
    Device.close_all()
    print("Exit")

atexit.register(cleanup)

async def main(t: ATrike):
    # section: center streering
    # await t.set_steering(constants.SERVO_MID)

    # # section: concurrent beeping and moving
    # await asyncio.gather(
    #     t.beep_every_second(5),
    #     t.move_forward(0.15, 5)
    # )
    # # section turn wheel sharply and slow down
    # await t.set_steering(constants.SERVO_LEFT)
    # await t.move_forward(0.15, 5)
    # section: just beeping
    await t.constant_beep(1)



if __name__ == "__main__":
    hardware = Hardware()
    trike = ATrike(hardware)
    asyncio.run(main(trike))
    hardware.reset()

