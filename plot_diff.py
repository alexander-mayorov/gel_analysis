import os
from PIL import Image
import numpy as np
import pylab
from scipy.optimize import curve_fit
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc


#params:
pxse = 133
pys = 42
pye = 162
ppix = 120
phwidth = 0
mm = 22./174
path = '/Users/aleksandrmaiorov/Desktop/methylene_blue'
tif_file = 'IMG_0282_1.tif'

def sigmoid(x, x0, k, L):
     y = 15 + L/ (1 + np.exp(-k*(x-x0)))
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

params = []
xdata = np.linspace(0,float(ppix)*mm,ppix)
times = []
os.chdir(path)
image1 = Image.open(tif_file)
image1.load()
frame_nmb = image1.n_frames
for framen in range(0, frame_nmb, 1):
    image1.seek(framen)
    profile = lin_profile(pxse, pys, pye, phwidth)
    ydata = np.array(profile[:ppix])
    try:
        maxim = ydata.max()
        minim = ydata.min()
        indmin = ydata.tolist().index(minim)
        popt, pcov = curve_fit(sigmoid, xdata[indmin:], ydata[indmin:], p0=[1, 1, maxim])
        y = sigmoid(xdata, *popt)
        if popt[0] > 0:
            params.append({'x0' : popt[0], 'k' : popt[1],
                      'L' : popt[2]})
            times.append(framen*12./60.)
    except RuntimeError:
        print("unable to fit at frame %d"%framen)
half_values=[(x['x0']*mm)**2 for x in params]
plt.plot(times, half_values)
plt.xlabel('time (min)')
plt.ylabel('distance(mm^2)')
plt.show()
f = open(tif_file.replace('.tif', '.csv'), 'w')
f.write('#time(min)\tdistance(mm)\n')
for i in range(0,len(half_values)):
    f.write('%(time)f\t%(distance)f\n'%{'time':times[i],
            'distance':half_values[i]})
f.close()
