import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import ticker
from matplotlib.colors import LinearSegmentedColormap
from glob import glob

def Stich(cv_img , folder_name):
    dim = [1024, 768]
    sticther = cv2.Stitcher.create()
    ret, pano = sticther.stitch(cv_img)
    if ret == cv2.STITCHER_OK:
        cv2.imwrite('static/{}_NIR.jpg'.format(folder_name), pano)
        cv2.waitKey()
        cv2.destroyAllWindows()
        return '{}_NIR.jpg'.format(folder_name)

    else:
        return "Error during Stitching. Please Input Correct Images"
