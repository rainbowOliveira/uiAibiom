import itk
import vtk
import os
from os import listdir

# Estrutura do projeto.
project_dir = os.getcwd()
DiretoriaDataSets = os.path.join(project_dir, "DataSets")
DiretoriaItkOutput = os.path.join(project_dir, "ItkOutput")
DiretoriasDataSets = []

# ITK Image type.
Dimension = 3
PixelType = itk.US
ImageType = itk.Image[PixelType, Dimension]

# ITK Image reader.
itkReader = itk.ImageFileReader[ImageType].New()
# ITK Image writer.
writer = itk.ImageFileWriter[ImageType].New()
# VTK Image reader.
vtkReader = vtk.vtkStructuredPointsReader()

# ITK filters.
binaryThreshold = itk.BinaryThresholdImageFilter[ImageType, ImageType].New()

# VTK colours.
colors = vtk.vtkNamedColors()
# VTK mapper.
mapper = vtk.vtkDataSetMapper()
# VTK actor.
actor = vtk.vtkActor()
# VTK renderer.
renderer = vtk.vtkRenderer()
# VTK renderer_window.
renderer_window = vtk.vtkRenderWindow()
# VTK renderer_window_interactor.
interactor = vtk.vtkRenderWindowInteractor()
# VTK transverse plan widget.
transverse_widget = vtk.vtkImagePlaneWidget()
# VTK coronal plan widget.
coronal_widget = vtk.vtkImagePlaneWidget()
# VTK coronal sagittal widget.
sagittal_widget = vtk.vtkImagePlaneWidget()
# VTK isosurface
iso = vtk.vtkMarchingCubes()

# Lista que armazena os itk datasets.
dataSets = []

def carregarDiretoriasDataSets():

    # Carregam-se as diretorias de todos os datasets.
    for diretoriaDataSet in listdir(DiretoriaDataSets):
        DiretoriasDataSets.append(os.path.join(DiretoriaDataSets, diretoriaDataSet))
    print(DiretoriasDataSets)

def carregarDataSets():

    # Carregam-se todos os datasets.
    for diretoriaDataSet in DiretoriasDataSets:
        itkReader.SetFileName(diretoriaDataSet)
        itkReader.Update()
        dataSets.append(itkReader.GetOutput())
    print(dataSets)

def binaryThresholdFun(itkImage, label):

    outsideValue = 0
    insideValue = 1

    binaryThreshold.SetLowerThreshold(label)
    binaryThreshold.SetUpperThreshold(label)
    binaryThreshold.SetOutsideValue(outsideValue)
    binaryThreshold.SetInsideValue(insideValue)
    binaryThreshold.SetInput(itkImage)
    binaryThreshold.Update()

def writeItkImage(itkImage):

    writer.SetInput(itkImage)
    writer.SetFileName(os.path.join(DiretoriaItkOutput, "output.vtk"))
    writer.Update()

def displayVtkFile(vtkDir):

    vtkReader.SetFileName(vtkDir)
    vtkReader.Update()

    iso.SetInputConnection(vtkReader.GetOutputPort())
    iso.SetValue(0, 1)

    # Map the surface to graphics primitives
    mapper.SetInputConnection(iso.GetOutputPort())

    # Create an actor to represent the surface
    actor.SetMapper(mapper)

    # Define the rendering window
    renderer_window.AddRenderer(renderer)
    renderer.SetBackground(0.1, 0.2, 0.4)

    # Define the interactor
    interactor.SetRenderWindow(renderer_window)

    # Sagital
    sagittal_widget.SetInteractor(interactor)
    sagittal_widget.RestrictPlaneToVolumeOn()
    sagittal_widget.SetInputConnection(vtkReader.GetOutputPort())
    sagittal_widget.SetPlaneOrientationToXAxes()
    sagittal_widget.SetSliceIndex(100)
    sagittal_widget.DisplayTextOn()
    sagittal_widget.SetDefaultRenderer(renderer)
    sagittal_widget.SetTexturePlaneProperty(actor.GetProperty())
    sagittal_widget.TextureInterpolateOff()
    sagittal_widget.SetPicker(None)
    sagittal_widget.On()

    # Tranversal
    coronal_widget.SetInteractor(interactor)
    coronal_widget.RestrictPlaneToVolumeOn()
    coronal_widget.SetInputConnection(vtkReader.GetOutputPort())
    coronal_widget.SetPlaneOrientationToYAxes()
    coronal_widget.SetSliceIndex(32)
    coronal_widget.DisplayTextOn()
    coronal_widget.SetDefaultRenderer(renderer)
    coronal_widget.SetTexturePlaneProperty(actor.GetProperty())
    coronal_widget.TextureInterpolateOff()
    coronal_widget.SetPicker(None)
    coronal_widget.On()

    # Coronal
    transverse_widget.SetInteractor(interactor)
    transverse_widget.RestrictPlaneToVolumeOn()
    transverse_widget.SetInputConnection(vtkReader.GetOutputPort())
    transverse_widget.SetPlaneOrientationToZAxes()
    transverse_widget.SetSliceIndex(100)
    transverse_widget.DisplayTextOn()
    transverse_widget.SetDefaultRenderer(renderer)
    transverse_widget.SetTexturePlaneProperty(actor.GetProperty())
    transverse_widget.TextureInterpolateOff()
    transverse_widget.SetPicker(None)
    transverse_widget.On()

    # Initialize the interactor and start the rendering loop
    renderer_window.SetSize(800, 800)
    renderer_window.Render()
    interactor.Start()

if __name__ == "__main__":

    carregarDiretoriasDataSets()
    carregarDataSets()
    binaryThresholdFun(dataSets[0], 2)
    writeItkImage(binaryThreshold.GetOutput())
    displayVtkFile(DiretoriasDataSets[0])
