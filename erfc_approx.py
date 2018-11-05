import os
from PIL import Image
import numpy as np
import pylab
from scipy.optimize import curve_fit
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

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

def sigmoid(x, x0, k, L):
     y = k*erfc((x-x0)/L)
     return y

def lin_profile(xse=92, ys=39, ye=139, hwidth=2):
    profile = []
    hor = []
    for i in range(ys, ye, 1):
        for j in range(xse-5, xse+5, 1):
            hor.append(image1.getpixel((j, i)))
        profile.append(np.average(hor))
    return profile

os.chdir('/Users/aleksandrmaiorov/Desktop/methylene_blue')
os.getcwd()
params = []
image1 = Image.open('Result_IMG_0275.tif')
image1.load()
frame_nmb = image1.n_frames
xdata = np.linspace(0,100,100)
step = frame_nmb / 5
i=0
for framen in range(0, frame_nmb, step):
    image1.seek(framen)
    profile = lin_profile()
    ydata = np.array(profile[:100])
    try:
        popt, pcov = curve_fit(sigmoid, xdata, ydata, p0=[0, ydata.max(), 1])
        y = sigmoid(xdata, *popt)
        params.append({'x0' : popt[0], 'k' : popt[1], 'L' : popt[2]})
        time = framen*12/60
        pylab.plot(xdata, ydata, 'o', color = colors[i], label='%.1f' % time)
        pylab.plot(xdata,y, color = colors[i])
    except RuntimeError:
        params.append({'x0' : 0, 'k' : 0, 'L' : 0})
        time = framen*12/60
        pylab.plot(xdata, ydata, 'o', color = colors[i], label='%.1f' % time)
        print("unable to fit at frame %d"%framen)
    i+=1
pylab.legend(title='time(min)', loc='best')
plt.xlabel('distance(pix)')
plt.ylabel('pixel value')
pylab.show()
