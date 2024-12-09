from hardware import Hardware
from atrike import ATrike
import asyncio
import atexit
import constants


async def main(t: ATrike):
    #asyncio.create_task(t.log_distance())
    asyncio.create_task(t.poll_distance())
    asyncio.create_task(t.beep_distance1())
    await t.set_steering(constants.SERVO_MID)
    await asyncio.Future() # wait indefinitely
    
    # # await t.set_steering(constants.SERVO_LEFT)

    # await t.move_forward(0.15, 5)
    
    # await t.constant_beep(1)


if __name__ == "__main__":
    try:
        hardware = Hardware()
        trike = ATrike(hardware)
        asyncio.run(main(trike))
    except KeyboardInterrupt:
        hardware.reset()
    except:
        hardware.reset()
    finally:
        hardware.reset()
    print("Exit Exit")

