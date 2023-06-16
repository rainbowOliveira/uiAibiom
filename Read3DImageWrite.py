""" Read3DImageWrite.py """

import itk
import pandas
import numpy as np

inputFilename  = "../input/BH0030.nii"
outputFilename = "../input/BH0030.vtk"

# ITK Image type
Dimension = 3
PixelType = itk.SS
ImageType = itk.Image[PixelType, Dimension]

# Read ITK Image
print ("Reading:", inputFilename)
reader = itk.ImageFileReader[ImageType].New()
reader.SetFileName( inputFilename )
reader.Update()

img = ImageType.New()
img = reader.GetOutput()

# Get some ITK Image Info
origin  = img.GetOrigin()
spacing = img.GetSpacing()
region  = img.GetRequestedRegion()
size    = region.GetSize()
start   = region.GetIndex()

print ("ITK Input Image Info:")
print ("  origin  =", origin)
print ("  spacing =", spacing)
print ("  size    =", size)
print ("  start   =", start)
print ("")

# filtering
# ...


dX = spacing[0]
dY = spacing[1]
dZ = spacing[2]
dV = dX*dY*dZ
print("dV (mm3)", dV)
print("dV (mm3)", np.prod(spacing))

Nx = size[0] # nº pixels na direcao 0
Ny = size[1] # nº pixels na direcao 0
Nz = size[2] # nº pixels na direcao 0

N_tot = Nx*Ny*Nz
print("N_tot (pix)", N_tot)

# Write ITK Image
print ("Writing:", outputFilename)
writer = itk.ImageFileWriter[ImageType].New()
#writer.SetInput( reader.GetOutput() )
writer.SetInput( img )
writer.SetFileName( outputFilename )
writer.Update()

print ("EOF.")