import pickle
import subprocess
import numpy as np
from mux import Mux
from adc import Ltc2312
from ke24xx import Ke24xx

smu = Ke24xx('10.10.32.1', 24)
mux = Mux()
adc = Ltc2312()

smu.forceVoltage()
smu.setComplianceI(0.01)
smu.setVoltage(0)

inputVoltages = np.linspace(0, 20, 21)
vCellMid = np.zeros_like(inputVoltages)
vCellHi = np.zeros_like(inputVoltages)

with smu.keepOutputOnDuring():
    for name, data, muxFunction in zip(['mid', 'hi'],
                                       [vCellMid, vCellHi],
                                       [mux.selectVoltageCellMid,
                                        mux.selectVoltageCellHi]):
        input(f'connect smu to v_cell_{name} ')
        muxFunction()
        for index, voltage in enumerate(inputVoltages):
            smu.setVoltage(voltage)
            data[index] = adc.convert()

picklefilename = 'analog_in_data.pickle'
with open(picklefilename, 'wb') as fh:
    pickle.dump(inputVoltages, fh)
    pickle.dump(vCellMid, fh)
    pickle.dump(vCellHi, fh)

subprocess.Popen(['python', 'plot_analog_in.py', picklefilename])
