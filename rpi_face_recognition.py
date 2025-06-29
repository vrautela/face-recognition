#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# BCM pin number that the PIR sensor's OUT pin is connected to
# TODO: change this to be a command line argument
PIR_PIN = 17

# Callback function to be called when motion is detected
def motion_detected(channel):
    # TODO: this is where I will put the video recording and analysis code
    # I'm not sure if this is a situtation where I would benefit from a more concurrent solution
    # It might be nice if I could record a second of video then analyze it and repeat that process N times
    print("Motion detected! Running event handler...")

def main():
    # Use BCM (Broadcom) pin numbering
    GPIO.setmode(GPIO.BCM)
    
    # Set PIR_PIN as an input
    GPIO.setup(PIR_PIN, GPIO.IN)

    # Give the PIR sensor some time to settle after powering up
    print("Waiting for PIR sensor to stabilize (2 sec)...")
    time.sleep(2)
    print("Ready for motion detection.")

    # Configure event detection on a rising edge:
    # - "GPIO.RISING" means the callback is triggered when the pin goes from LOW to HIGH
    # - bouncetime helps prevent bouncing (false rapid triggers) within the specified timeframe (ms)
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected, bouncetime=300)

    try:
        # Keep the main thread alive so callbacks can occur
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()


