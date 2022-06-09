
# %%
import os
import numpy as np
import pydicom 
import cv2
import matplotlib.pyplot as plt 
from scipy import ndimage
from skimage import filters


# %%
PathDicom = "./database2"
lstFilesDCM = []  
lstProcessed = []
i = 0
#search for dicom files.
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        img = plt.imread(dirName+'/'+filename, format='RGB').astype(np.float64)
        if img.shape != (512, 512, 3):
            if img.shape != (512 , 512 ):
                print(img.shape)
                print(dirName+'  '+ filename)
                os.remove(dirName+'/'+filename)
                
print(i)

# %%
