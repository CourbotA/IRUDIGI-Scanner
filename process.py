import os
import numpy
import pydicom 
import matplotlib.pyplot as plt 

PathDicom = "./CT+MR 1/"
lstFilesDCM = []  

#search for dicom files.
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))
            
# Get ref file
for elem in lstFilesDCM:
    medical_image = pydicom.read_file(elem)
    image = medical_image.pixel_array
    medical_image.default_element_format
    plt.imshow(image,cmap='gray')
    print(medical_image.file_meta.MediaStorageSOPClassUID.name)

