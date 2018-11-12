import os
from PIL import Image
import numpy as np
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

#params:
pxse = 131
pys = 67
pye = 125
ppix = pye-pys
phwidth = 0
mm = 22./174
path = '/Users/aleksandrmaiorov/Desktop/methylene_blue/Flat_images'
tif_file = 'Result_IMG_0282.tif'
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

def erfc_profile(x, L, t, ag):
    return 0.5*erfc((x - ag*t)/L)

def read_images(pathm, file_name, xse=92, ys=56, ye=156, hwidth=2):
    os.chdir(path)
    image1 = Image.open(tif_file)
    image1.load()
    frame_nmb = image1.n_frames
    profiles = []
    for framen in range(0, frame_nmb, 1):
        image1.seek(framen)
        profile = []
        hor = []
        if hwidth !=0:
            for i in range(ys, ye, 1):
                for j in range(xse-hwidth, xse+hwidth, 1):
                    hor.append(float(image1.getpixel((j, i))))
                    profile.append(np.average(hor))
        else:
            for i in range(ys, ye, 1):
                profile.append(float(image1.getpixel((xse, i))))
        profiles.append(profile)
    return profiles

def normalize(profiles):
    max = np.amax(np.array(profiles))
    normalized = profiles/max
    return normalized

def plot_profiles(xdata, nprofiles):
    plen = len(profiles)
    xdata = np.linspace(0,float(ppix)*mm,ppix)
    i=0
    for framen in range(0, plen, plen/5):
        time = framen*12/60
        try:
            popt, pcov = curve_fit(erfc_profile, xdata, nprofiles[framen])
            y = erfc_profile(xdata, *popt)
            plt.plot(xdata, nprofiles[framen], '.', color = colors[i],
                     label='%.1f' % time)
            plt.plot(xdata,y, color = colors[i])
        except RuntimeError:
            plt.plot(xdata, nprofiles[framen], '.', color = colors[i],
                     label='%.1f' % time)
            print("unable to fit at frame %d"%framen)
        i=i+1
    plt.legend(title='time(min)', loc='best')
    plt.xlabel('distance(mm)')
    plt.ylabel('pixel value')
    plt.show()
    return

profiles = read_images(path, tif_file, pxse, pys, pye, phwidth)
nprofiles = normalize(profiles)
plot_profiles(nprofiles)
