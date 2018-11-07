import os
from PIL import Image
import numpy as np
import pylab
from scipy.optimize import curve_fit
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

#params:
pxse = 100
pys = 69
pye = 139
ppix = 70
phwidth = 0
mm = 22./174
path = '/Users/aleksandrmaiorov/Desktop/methylene_blue'
tif_file = 'IMG_0303.tif'
colors = ['#1f77b4',
          '#ff7f0e',
          '#2ca02c',
          '#d62728',
          '#9467bd',
          '#8c564b',
          '#e377c2',
          '#7f7f7f',
          '#bcbd22',
          '#17becf',
          '#1a55FF']

def sigmoid(x, x0, k, L, y0):
     y = 20 + L/ (1 + np.exp(-k*(x-x0)))
     return y

def erf_sigmoid(x, x0, k, L):
    y = x0 + k*erf((x)/L)
    return y

def lin_profile(xse=92, ys=56, ye=156, hwidth=2):
    profile = []
    hor = []
    if hwidth !=0:
        for i in range(ys, ye, 1):
            for j in range(xse-hwidth, xse+hwidth, 1):
                hor.append(image1.getpixel((j, i)))
            profile.append(np.average(hor))
    else:
        for i in range(ys, ye, 1):
            profile.append(image1.getpixel((xse, i)))
    return profile

os.chdir(path)
os.getcwd()
params = []
image1 = Image.open(tif_file)
image1.load()
frame_nmb = image1.n_frames
xdata = np.linspace(0,float(ppix)*mm,ppix)
step = frame_nmb / 5
i=0
for framen in range(0, frame_nmb, step):
    image1.seek(framen)
    profile = lin_profile(pxse, pys, pye, phwidth)
    ydata = np.array(profile[:ppix])
    try:
        maxim = ydata.max()
        minim = ydata.min()
        indmin = ydata.tolist().index(minim)
        popt, pcov = curve_fit(sigmoid, xdata[indmin:], ydata[indmin:], p0=[1, 1, maxim, minim])
        y = sigmoid(xdata, *popt)
        params.append({'x0' : popt[0], 'k' : popt[1], 'L' : popt[2]})
        time = framen*12/60
        pylab.plot(xdata, ydata, '.', color = colors[i], label='%.1f' % time)
        pylab.plot(xdata,y, color = colors[i])
    except RuntimeError:
        params.append({'x0' : 0, 'k' : 0, 'L' : 0})
        time = framen*12/60
        pylab.plot(xdata, ydata, '.', color = colors[i], label='%.1f' % time)
        print("unable to fit at frame %d"%framen)
    i+=1
pylab.legend(title='time(min)', loc='best')
plt.xlabel('distance(mm)')
plt.ylabel('pixel value')
pylab.show()
