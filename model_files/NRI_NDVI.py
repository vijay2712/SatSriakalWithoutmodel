import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import ticker
from matplotlib.colors import LinearSegmentedColormap
import glob

def Ndvi(truepano , imageName):
    output_name = 'static/{}_NDVI.{}'.format(imageName.split(".")[0] ,imageName.split(".")[1])
    image = truepano
    nir = (image[:, :, 0]).astype('float')
    r = (image[:, :, 2]).astype('float')
    ndvi = np.zeros(r.size)
    ndvi = np.true_divide(np.subtract(nir, r), np.add(nir, r))
    cols3 = ['gray','blue', 'green', 'yellow','red']
    norm = colors.Normalize(vmin=-1, vmax=1)
    # ndvi=ndvi/255
    fig, ax = plt.subplots(1, 1)
    im = ax.imshow(ndvi, cmap=LinearSegmentedColormap.from_list(name='custom1', colors=cols3), norm=norm)
    fig.colorbar(im)
    ax.yaxis.set_major_locator(plt.NullLocator())  # remove y axis ticks
    ax.xaxis.set_major_locator(plt.NullLocator())  # remove x axis ticks
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(output_name, dpi=600, transparent=True, bbox_inches=extent, pad_inches=0)
    return '{}_NDVI.{}'.format(imageName.split(".")[0] ,imageName.split(".")[1])




















