import RPi.GPIO as GPIO
import time

EchoPin = 0
TrigPin = 1

def distance():
    GPIO.output(TrigPin,GPIO.LOW)
    time.sleep(0.000001)  # One micro second
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000001)  # One micro second
    GPIO.output(TrigPin,GPIO.LOW)
    start_waiting_for_echo = time.time()
    while not GPIO.input(EchoPin):
        waiting_for_echo = time.time()
        if (waiting_for_echo - start_waiting_for_echo) > 0.03 :
            return -1 # time-out

    echo_start = time.time()
    while GPIO.input(EchoPin):
        waiting_for_echo_end = time.time()
        if(waiting_for_echo_end - echo_start) > 0.03 :
            return -1 # time out

    echo_end = time.time()
    echo_duration = echo_end - echo_start
    time.sleep(0.01)
    return echo_duration * 17150  # Speed of sound * time / 2

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EchoPin,GPIO.IN)
    GPIO.setup(TrigPin,GPIO.OUT)
    while True:
        cm_dist = distance()
        print(f"{round(cm_dist, 2)}")


# ---
# import RPi.GPIO as GPIO
# import time

# GPIO.setmode(GPIO.BCM)

# TRIG = 0  # transmit pin
# ECHO = 1  # receive pin

# # Setup pins
# GPIO.setup(TRIG, GPIO.OUT)
# GPIO.setup(ECHO, GPIO.IN)

# def get_distance():
#     # Ensure trigger is low
#     GPIO.output(TRIG, False)
#     time.sleep(0.01)  # Short delay to settle
    
#     # Send trigger pulse
#     GPIO.output(TRIG, True)
#     time.sleep(0.00001)  # 10 microsecond pulse
#     GPIO.output(TRIG, False)
#     print("x")
#     # Get timing
#     while GPIO.input(ECHO) == 0:
#         pulse_start = time.time()
        
#     print("y")
#     while GPIO.input(ECHO) == 1:
#         pulse_end = time.time()
    
#     print("z")
#     # Calculate distance
#     pulse_duration = pulse_end - pulse_start
#     distance = pulse_duration * 17150  # Speed of sound * time / 2
    
#     return round(distance, 2)  # Return in centimeters

# try:
#     while True:
#         dist = get_distance()
#         print(f"Distance: {dist} cm")
#         time.sleep(1)
# except:
#     GPIO.cleanup()
