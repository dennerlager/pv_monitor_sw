import atexit
import struct
import unittest
from smbus2 import SMBus

class Lm73:
    memory = {'temperature': 0,
              'configuration': 1,
              'thigh': 2,
              'tlow': 3,
              'control-status': 4,
              'identification': 7, }
    temperatureFormat = struct.Struct('>h')
    def __init__(self):
        self.bus = SMBus(1)
        self.address = 0x48
        self.powerDown()
        atexit.register(self.bus.close)

    def powerDown(self):
        self.bus.write_byte_data(self.address,
                                 self.memory['configuration'],
                                 0x80)

    def getTemperature(self):
        self.triggerOneShot()
        self.waitForData()
        return self.translateToTemperature(
            self.bus.read_word_data(self.address,
                                    self.memory['temperature']))

    def triggerOneShot(self):
        self.bus.write_byte_data(self.address,
                                 self.memory['configuration'],
                                 0x84)

    def waitForData(self):
        for _ in range(10):
            if self.bus.read_byte_data(self.address,
                                       self.memory['control-status']) & 1:
                break
        else:
            raise RuntimeError('temperature read time out')

    def translateToTemperature(self, registerValues):
        return self.temperatureFormat.unpack(registerValues)[0] >> 7

class TestLm37(unittest.TestCase):
    def setUp(self):
        self.tempsens = Lm73()

    def test_translateToTemperature(self):
        self.assertEqual(
            150, self.tempsens.translateToTemperature(bytes([0x4b, 0])))
        self.assertEqual(
            1, self.tempsens.translateToTemperature(bytes([0, 0x80])))
        self.assertEqual(
            0, self.tempsens.translateToTemperature(bytes([0, 0])))
        self.assertEqual(
            -1, self.tempsens.translateToTemperature(bytes([0xff, 0x80])))
        self.assertEqual(
            -40, self.tempsens.translateToTemperature(bytes([0xec, 0])))
