# External module imports
import RPi.GPIO as GPIO
import controller
import datetime
import time
from signal import signal, SIGINT
from sys import exit

FREQ = 100
R_PIN_NUM = 3
B_PIN_NUM = 5
G_PIN_NUM = 7
W_PIN_NUM = 8

def main():
    print("Initializing LEDs")

    # Pin setup:
    GPIO.setmode(GPIO.BOARD)  # Use numbering scheme for physical pins on board, not GPIO labels

    r_led = init_led(R_PIN_NUM)
    g_led = init_led(G_PIN_NUM)
    b_led = init_led(B_PIN_NUM)
    w_led = init_led(W_PIN_NUM)

    # Tell Python to run the cleanup() function when SIGINT (CTRL+c) is recieved
    signal(SIGINT, lambda s, f: cleanup(s, f, [r_led, g_led, b_led, w_led]))

    # Set brightness for each LED color:
    while True:
        rgbw = controller.get_color_at_datetime(datetime.datetime.now())

        r_led.ChangeDutyCycle(float(rgbw[0]) / 2.55)
        g_led.ChangeDutyCycle(float(rgbw[1]) / 2.55)
        b_led.ChangeDutyCycle(float(rgbw[2]) / 2.55)
        w_led.ChangeDutyCycle(float(rgbw[3]) / 2.55)
        time.sleep(60)


def init_led(ledPin):
    GPIO.setup(ledPin, GPIO.OUT)
    p = GPIO.PWM(ledPin, FREQ)
    p.start(0)
    return p


def cleanup(signal_received, frame, pins):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    for p in pins:
        p.stop()

    GPIO.cleanup()
    exit(0)


if __name__ == '__main__':
    main()

