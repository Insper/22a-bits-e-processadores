#!/usr/bin/env python3

from myhdl import block, always_comb


@block
def sevenSeg(bcd, leds):
    @always_comb
    def comb():
        if bcd == 0:
            leds.next = 0b1000000
        elif bcd == 1:
            leds.next = 0b1111001
        elif bcd == 2:
            leds.next = 0b0100100
        elif bcd == 3:
            leds.next = 0b0110000
        elif bcd == 4:
            leds.next = 0b0011001
        elif bcd == 5:
            leds.next = 0b0010010
        elif bcd == 6:
            leds.next = 0b0000010
        elif bcd == 7:
            leds.next = 0b1111000
        elif bcd == 8:
            leds.next = 0b0000000
        elif bcd == 9:
            leds.next = 0b0010000
        elif bcd == 10:
            leds.next = 0b0001000
        elif bcd == 11:
            leds.next = 0b0000011
        elif bcd == 12:
            leds.next = 0b1000110
        elif bcd == 13:
            leds.next = 0b0100001
        elif bcd == 14:
            leds.next = 0b0000110
        else:
            leds.next = 0b0001110

    return comb
