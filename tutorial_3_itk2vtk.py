'''
AIBIOM Computer Exercises
ERASMUS 2023 @ Lodz
Carlos Vinhais

tutorial_3_itk2vtk.py

1. Read ITK input image from VTK file
2. Get ITK image info
3. Process input image ... 
4. Connect ITK to VTK
5. Get VTK image info, and check with ITK
6. Process input image ...
7. Write output VTK polydata (mesh) to VTK file

'''

import itk
import vtk

print('tutorial_3_itk2vtk.py')

#inputFilename   = './BH0030.vtk'
inputFilename   = './mask.vtk'
#outputFilename1 = './mesh_clipped.vtk'


# # --------------------------------------------------
# # Read input ITK Image
# # --------------------------------------------------
# # ITK Image type (MRA grayscale image)
# Dimension = 3
# PixelType = itk.US
# ImageType = itk.Image[PixelType, Dimension]

# print ( 'Reading:', inputFilename )
# reader = itk.ImageFileReader[ImageType].New()
# reader.SetFileName( inputFilename )
# reader.Update()

# itkimg = ImageType.New()
# itkimg = reader.GetOutput()

# # ITK Image Info
# # --------------------------------------------------
# origin  = itkimg.GetOrigin()
# spacing = itkimg.GetSpacing()
# region  = itkimg.GetRequestedRegion()
# start   = region.GetIndex()
# size    = region.GetSize()

# print ('ITK Image Info:')
# print ('  origin  =', origin )
# print ('  spacing =', spacing )
# print ('  size    =', size )
# print ('  start   =', start )
# print ('')

# Process ITK Image
# --------------------------------------------------
# ...


# # --------------------------------------------------
# # Connect ITK and VTK
# # --------------------------------------------------
# # ITK to VTK: itk.ImageToVTKImageFilter
# # VTK to ITK: itk.VTKImageToImageFilter

# print ('ITK Image To VTK ImageData')
# itk2vtk = itk.ImageToVTKImageFilter[ImageType].New()
# itk2vtk.SetInput( itkimg )
# itk2vtk.Update()

# vtkimg = vtk.vtkImageData()
# vtkimg = itk2vtk.GetOutput()


# # --------------------------------------------------
# # ITK class ImageToVTKImageFilter not working in my laptop...
# # 2n OPTION: Read image with VTK...
# # --------------------------------------------------
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName( inputFilename )
reader.Update()

vtkimg = vtk.vtkImageData()
vtkimg = reader.GetOutput()
    
# VTK Image Info
# --------------------------------------------------
origin  = vtkimg.GetOrigin()
spacing = vtkimg.GetSpacing()
size    = vtkimg.GetDimensions()
bounds  = vtkimg.GetBounds()
extent  = vtkimg.GetExtent()
vrange  = vtkimg.GetPointData().GetScalars().GetValueRange()

print ('VTK Image Info:')
print ('origin  =', origin )
print ('spacing =', spacing )
print ('size    =', size )
print ('bounds  =', bounds )
print ('extent  =', extent )
print ('vrange  =', vrange )
print ('')


# # --------------------------------------------------
# # Process VTK Image
# # --------------------------------------------------
# print( 'Outline' )

outlineFilter = vtk.vtkOutlineFilter()
outlineFilter.SetInputData( vtkimg )
outlineFilter.Update()

outline = vtk.vtkPolyData()
outline = outlineFilter.GetOutput()

# print('Contour' )

isovalue = 0.5
contourFilter = vtk.vtkContourFilter()
contourFilter.SetValue(0, isovalue)
contourFilter.SetInputData( vtkimg )
contourFilter.Update()

isosurface = vtk.vtkPolyData()
isosurface = contourFilter.GetOutput()
        
# print('Clip with sphere' )

# center = [0, 0, -32] # mm
# radius = 50 # mm
# sphere = vtk.vtkSphere()
# sphere.SetCenter( center )
# sphere.SetRadius( radius )
   
# clip = vtk.vtkClipPolyData()
# clip.SetClipFunction( sphere )
# clip.SetInputData( isosurface )
# clip.SetInsideOut( 1 )
# clip.Update()

# clipped = vtk.vtkPolyData()
# clipped = clip.GetOutput(0)


# print('Connectivity' )

# # Extract Largest Isosurface
# connectivity1 = vtk.vtkPolyDataConnectivityFilter()
# connectivity1.SetInputData( clipped )
# connectivity1.SetExtractionModeToLargestRegion()
# connectivity1.Update()

# largest = vtk.vtkPolyData()
# largest = connectivity1.GetOutput()

# # Extract Closest Isosurface
# P = [0, 0, -32] # mm
# connectivity2 = vtk.vtkPolyDataConnectivityFilter()
# connectivity2.SetInputData( clipped )
# connectivity2.SetExtractionModeToClosestPointRegion()
# connectivity2.SetClosestPoint ( P )
# connectivity2.Update()

# closest = vtk.vtkPolyData()
# closest = connectivity2.GetOutput()


# # --------------------------------------------------
# # VTK visuialization pipeline
# # --------------------------------------------------

# Create mappers
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData( outline )
mapper.ScalarVisibilityOff()


mapper1 = vtk.vtkPolyDataMapper()
mapper1.SetInputData( isosurface )
mapper1.ScalarVisibilityOff()

# mapper2 = vtk.vtkPolyDataMapper()
# mapper2.SetInputData( largest )
# mapper2.ScalarVisibilityOff()

# # Create actors, and connect mappers
actor = vtk.vtkActor()
actor.SetMapper( mapper )
actor.GetProperty().SetColor(1,1,1) # RGB
actor.GetProperty().SetOpacity( 0.5 )

actor1 = vtk.vtkActor()
actor1.SetMapper( mapper1 )
actor1.GetProperty().SetColor(1,1,0) # RGB
actor1.GetProperty().SetOpacity( 1 )

# actor2 = vtk.vtkActor()
# actor2.SetMapper( mapper2 )
# actor2.GetProperty().SetColor(1,0,0) # RGB
# actor2.GetProperty().SetOpacity( 0.5 )

# Create a renderer, and add actors to it
ren = vtk.vtkRenderer()
ren.SetBackground(0.25,0.25,0.25) # RGB
ren.AddActor( actor )
ren.AddActor( actor1 )
#ren.AddActor( actor2 )

# # Create a render window
renwin = vtk.vtkRenderWindow()
renwin.SetSize( 512, 512 )
renwin.AddRenderer( ren )

# # Create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow( renwin )

# # --------------------------------------------------

# # render and enable user interface interactor
iren.Initialize()
renwin.Render()
renwin.SetWindowName( 'Exercise 3' )
iren.Start()

# # --------------------------------------------------
# # Write output VTK PolyData
# # --------------------------------------------------
# print ( 'Writing VTK polydata:', outputFilename1 )
# writer = vtk.vtkPolyDataWriter()
# writer.SetInputData( clipped )    
# writer.SetFileName( outputFilename1 )
# writer.Write()



print('EOF.')