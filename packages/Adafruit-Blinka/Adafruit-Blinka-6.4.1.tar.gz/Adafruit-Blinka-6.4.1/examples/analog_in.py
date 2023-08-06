"""Analog in demo"""
import time
import board
from analogio import AnalogIn

analog_in = AnalogIn(board.A1)


def get_voltage(pin):
    return (pin.value * 3.3) / 4096


while True:
    print((get_voltage(analog_in),))
    time.sleep(0.1)
