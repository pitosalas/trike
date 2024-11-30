
Sequence
    together
        do for 5 seconds
            beep every second
        end

        do for 5 seconds
            move forward at speed x
        end
    end
    do for 5 seconds
        beep for 5 seconds
    end
end

from gpiozero import TonalBuzzer, Motor
import asyncio

async def beep_every_second(buzzer, duration):
    end_time = asyncio.get_event_loop().time() + duration
    while asyncio.get_event_loop().time() < end_time:
        buzzer.play('A4')
        await asyncio.sleep(0.1)  # Short beep
        buzzer.stop()
        await asyncio.sleep(0.9)  # Wait for remainder of second

async def move_forward(motor, speed, duration):
    motor.forward(speed)
    await asyncio.sleep(duration)
    motor.stop()

async def constant_beep(buzzer, duration):
    buzzer.play('A4')
    await asyncio.sleep(duration)
    buzzer.stop()

async def main():
    # Setup hardware
    buzzer = TonalBuzzer(8)
    motor = Motor(forward=19, backward=26, enable=13)

    # First section: concurrent beeping and moving
    await asyncio.gather(
        beep_every_second(buzzer, 5),
        move_forward(motor, 0.5, 5)
    )

    # Second section: just beeping
    await constant_beep(buzzer, 5)

# Run the sequence
asyncio.run(main())