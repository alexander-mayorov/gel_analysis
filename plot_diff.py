import os
from PIL import Image
import numpy as np
import pylab
from scipy.optimize import curve_fit
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc


pxse = 125
pys = 78
pye = 178
ppix = 100
phwidth = 1
mm = 22./174
path = '/Users/aleksandrmaiorov/Desktop/methylene_blue'
tif_file = 'Result_IMG_0276.tif'
def sigmoid(x, x0, k, L, y0):
     y = y0 + L/ (1 + np.exp(-k*(x-x0)))
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
        popt, pcov = curve_fit(sigmoid, xdata, ydata,
                               p0=[1, 1, ydata.max(), ydata.min()])
        y = sigmoid(xdata, *popt)
        if popt[0] > 0:
            params.append({'x0' : popt[0], 'k' : popt[1],
                      'L' : popt[2], 'y0' : popt[3]})
            times.append(framen*12./60.)
    except RuntimeError:
        print("unable to fit at frame %d"%framen)
half_values=[(x['x0']*mm)**2 for x in params]
plt.plot(times, half_values)
plt.xlabel('time (min)')
plt.ylabel('distance(mm^1/2)')
plt.show()
f = open(tif_file.replace('.tif', '.csv'), 'w')
f.write('#time(min)\tdistance(mm)\n')
for i in range(0,len(half_values)):
    f.write('%(time)f\t%(distance)f\n'%{'time':times[i],
            'distance':half_values[i]})
f.close()
