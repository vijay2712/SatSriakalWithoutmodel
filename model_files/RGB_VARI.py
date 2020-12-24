import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import ticker
from matplotlib.colors import LinearSegmentedColormap
import glob

def RGB(truepano , filename):
    image = truepano
    r = (image[:, :, 0]).astype('float')
    g = (image[:, :, 1]).astype('float')
    b = (image[:, :, 2]).astype('float')
    # formula for VARI: (Green - Red)/(Green + Red - Blue)
    Vari = np.zeros(r.size)
    Vari = np.true_divide((np.subtract(g, r)), (np.subtract(np.add(g, r), b)))
    norm = colors.Normalize(vmin=-1, vmax=1)
    cols3 = ['blue', 'red', 'green', 'yellow']
    output_name = 'static/{}_VARI.{}'.format(filename.split(".")[0], filename.split(".")[1])
    fig, ax = plt.subplots(1, 1)
    im = ax.imshow(Vari, cmap=LinearSegmentedColormap.from_list(name='custom1', colors=cols3), norm=norm)
    fig.colorbar(im)
    ax.yaxis.set_major_locator(plt.NullLocator())  # remove y axis ticks
    ax.xaxis.set_major_locator(plt.NullLocator())  # remove x axis ticks
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(output_name, dpi=600, transparent=True, bbox_inches=extent, pad_inches=0)
    return '{}_VARI.{}'.format(filename.split(".")[0],filename.split(".")[1])
