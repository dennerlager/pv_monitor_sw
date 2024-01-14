from gpiozero import DigitalOutputDevice

class Mux:
    addresses = {'vCellHi': 0,
                 'vCellMid': 1,
                 'iCellOut': 2,
                 'iCellIn': 3,
                 'spare': 4, }
    def __init__(self):
        self.address0 = DigitalOutputDevice(21)
        self.address1 = DigitalOutputDevice(20)
        self.address2 = DigitalOutputDevice(19)

    def setAddress(self, channel):
        address = self.addresses[channel]
        self.address0.value = address & 1
        self.address1.value = (address & 2) >> 1
        self.address2.value = (address & 4) >> 2

    def selectVoltageCellHi(self):
        self.setAddress('vCellHi')

    def selectVoltageCellMid(self):
        self.setAddress('vCellMid')

    def selectCurrentCellOut(self):
        self.setAddress('iCellOut')

    def selectCurrentCellIn(self):
        self.setAddress('iCellIn')

    def selectSpare(self):
        self.setAddress('spare')
