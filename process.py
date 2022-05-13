import os
import numpy
import pydicom 
import cv2
import matplotlib.pyplot as plt 

PathDicom = "./CT+MR 1/"
lstFilesDCM = []  

#search for dicom files.
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))
            

for elem in lstFilesDCM:
    processedName = (elem.split("\\")[-1].removesuffix('.dcm'))
    medical_image = pydicom.read_file(elem)
    image = medical_image.pixel_array
    
    plt.imshow(image,cmap='gray')
    if "MR" in processedName:
        plt.imsave('MR/'+processedName+'.png', image,cmap='gray')
    else :
        plt.imsave('CT/'+processedName+'.png', image,cmap='gray')
   
 
    
