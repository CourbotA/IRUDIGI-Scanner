import os
import sys
import cv2
from matplotlib.colors import Colormap
import numpy as np
import matplotlib.pyplot as plt2

import skimage.io
import skimage.color
import skimage.filters
from skimage import img_as_ubyte

pathCT = "./CT"

def select_object(seed, img, mask):
  
  f = [seed]
  while len(f) > 0:
    x_start, y_start = f.pop()
    for i,j in [(x_start - 1, y_start), (x_start - 1, y_start - 1), (x_start, y_start - 1), (x_start + 1, y_start - 1), (x_start + 1, y_start), (x_start + 1, y_start + 1), (x_start, y_start + 1), (x_start + 1, y_start - 1)]:
      if mask[i][j] == False and img[i][j][0] > 0:
        mask[i][j] = True
        f.append((i,j))

  return mask

for dir_path, dir_names, img_names in os.walk(pathCT):
    
    for name in img_names:
        img_path = os.path.join(dir_path, name)
        I = cv2.imread(img_path)
        
        # convert the image to grayscale
        gray_image = skimage.color.rgb2gray(I)

        # blur the image to denoise
        blurred_image = skimage.filters.gaussian(gray_image, sigma=1.0)

        # perform automatic thresholding
        t = skimage.filters.threshold_otsu(blurred_image)

        # create a binary mask with the threshold found by Otsu's method
        binary_mask = blurred_image > t

        # apply the binary mask to select the foreground
        imgT = I.copy()
        imgT[~binary_mask] = 0

        #select the object in the center of the image
        mask = binary_mask < 0
        seed = (212, 256)
        mask[212][256] = True

        mask = select_object(seed, imgT, mask)

        imgT[~mask] = 0
        
        #save the image in CT-tablefree
        plt2.imsave('CT-tablefree/' + name, imgT, cmap='gray')

