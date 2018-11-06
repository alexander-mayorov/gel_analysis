import os
from PIL import Image
import numpy as np
import pylab
from scipy.optimize import curve_fit
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

#params:
pxse = 108
pys = 51
pye = 117
ppix = 66
phwidth = 1
mm = 22./174
step = 20
path = '/Users/aleksandrmaiorov/Desktop/methylene_blue'
tif_file = 'IMG_0275.tif'

def sigmoid(x, x0, k, L):
     y = L / (1 + np.exp(-k*(x-x0)))
     return y

def lin_profile(xse=50, ys=88, ye=166):
    profile = []
    for i in range(ys, ye, 1):
        profile.append(image1.getpixel((50, i)))
    return profile

os.chdir(path)
params = []
image1 = Image.open(tif_file)
image1.load()
frame_nmb = image1.n_frames
xdata = np.linspace(0,ppix,ppix)
for framen in range(0, frame_nmb, step):
    image1.seek(framen)
    profile = lin_profile(pxse, pys, pye)
    ydata = np.array(profile[:ppix])
    try:
        popt, pcov = curve_fit(sigmoid, xdata, ydata, p0=[1, 1, ydata.max()])
        y = sigmoid(xdata, *popt)
        params.append({'x0' : popt[0], 'k' : popt[1], 'L' : popt[2]})
        time = framen*4/60
        pylab.plot(xdata, ydata, 'o', label='%.1f' % time)
        pylab.plot(xdata,y)
    except RuntimeError:
        params.append({'x0' : 0, 'k' : 0, 'L' : 0})
        time = framen*4/60
        pylab.plot(xdata, ydata, 'o', label='%.1f' % time)
pylab.legend(title='time(min)', loc='best')
plt.xlabel('distance(pix)')
plt.ylabel('pixel value')
pylab.show()
