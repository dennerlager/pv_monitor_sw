import atexit
import spidev

class Ltc2312:
    def __init__(self):
        self.vref_V = 2048
        self.bus = spidev.SpiDev(0, 0)
        self.bus.mode = 0
        atexit.register(self.bus.close)

    def nap(self):
        """two cs_b rising edges
        2mA"""
        for i in range(2):
            self.bus.xfer([])

    def sleep(self):
        """four cs_b rising edges
        0.2uA"""
        for i in range(4):
            self.bus.xfer([])

    def convert(self):
        return self.vref_V / (2**14 - 1) * (self.bus.readbytes(2) >> 2)

if __name__ == '__main__':
    adc = Ltc2312()
    input('convert? ')
    adc.convert()
    input('nap? ')
    adc.nap()
    input('sleep? ')
    adc.sleep()
