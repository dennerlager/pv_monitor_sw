import sys
import pickle
import subprocess
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf
import numpy.polynomial.polynomial as poly

picklefilename = sys.argv[1]
with open(picklefilename, 'rb') as fh:
    inputVoltages = pickle.load(fh)
    vCellMid = pickle.load(fh)
    vCellHi = pickle.load(fh)

pdffilename = picklefilename.replace('.pickle', '.pdf')
with pdf.PdfPages(pdffilename, 'w') as pdfh:
    for name, yvalues in zip(['mid', 'hi'],
                          [vCellMid, vCellHi]):
        figure, axes = plt.subplots(3, 1, figsize=(8.27, 11.69))
        ax0, ax1, ax2 = axes.ravel()
        ax0.plot(inputVoltages, yvalues, '-o')
        coefficients = poly.polyfit(inputVoltages, yvalues, 1)
        fit = poly.polyval(inputVoltages, coefficients)
        ax0.plot(inputVoltages, fit,
                label=(f'offset: {coefficients[0]:.3g}V\n' +
                       f'gain: {coefficients[1]:.3g}V/V'))
        ax0.legend()
        ax0.set_title(f'v_cell_{name}')
        ax0.set_ylabel('measured voltage (V)')

        error = yvalues - inputVoltages
        ax1.plot(inputVoltages, error, '-o')
        ax1.set_ylabel('measured voltage deviation (V)')

        relativeError = error / inputVoltages * 100
        ax2.plot(inputVoltages, relativeError, '-o')
        ax2.set_ylabel('measured voltage relative deviation (%)')
        ax2.set_xlabel('input voltage (V)')

        pdfh.savefig(figure)
        plt.close()

subprocess.Popen(['evince', pdffilename])
