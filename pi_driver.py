# External module imports
import pigpio
import controller
import datetime
import time
from signal import signal, SIGINT
from sys import exit
import numpy

FREQ = 100
R_PIN_NUM = 2
B_PIN_NUM = 3
G_PIN_NUM = 4
W_PIN_NUM = 14


def main():
    # connect to local Pi
    pi = pigpio.pi()

    # Tell Python to run the cleanup() function when SIGINT (CTRL+c) is recieved
    signal(SIGINT, lambda s, f: cleanup(s, f, pi))

    # Set brightness for each LED color:
    while True:
        rgbw = controller.get_color_at_datetime(datetime.datetime.now())
        (R, G, B, W) = numpy.multiply(rgbw, 2.55)

        pi.set_PWM_dutycycle(R_PIN_NUM, R)
        pi.set_PWM_dutycycle(G_PIN_NUM, G)
        pi.set_PWM_dutycycle(B_PIN_NUM, B)
        pi.set_PWM_dutycycle(W_PIN_NUM, W)

        time.sleep(5)


def cleanup(signal_received, frame, pi):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    pi.stop()
    exit(0)


if __name__ == '__main__':
    main()

