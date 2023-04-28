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

    # Read the source file.
    vtkReader.SetFileName(vtkDir)
    # vtkReader.ReadAllScalarsOn()  # Activate the reading of all scalars
    # vtkReader.ReadAllVectorsOn()  # Activate the reading of all vectors
    # vtkReader.ReadAllTensorsOn()  # Activate the reading of all tensors
    vtkReader.Update()  # Needed because of GetScalarRange
    output = vtkReader.GetOutput()
    scalar_range = output.GetScalarRange()

    # Create the mapper that corresponds the objects of the vtk file
    mapper.SetInputData(output)
    mapper.SetScalarRange(scalar_range)
    # mapper.ScalarVisibilityOff()

    # Create the Actor
    actor.SetMapper(mapper)
    actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().SetLineWidth(2.0)
    # actor.GetProperty().SetColor(colors.GetColor3d("MistyRose"))

    # backface = vtk.vtkProperty()
    # backface.SetColor(colors.GetColor3d('Tomato'))
    # actor.SetBackfaceProperty(backface)

    # Create the Renderer
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('Wheat'))

    # Create the RendererWindow
    renderer_window.SetSize(640, 480)
    renderer_window.AddRenderer(renderer)
    renderer_window.SetWindowName('ReadVtkFile')

    # Create the RendererWindowInteractor and display the vtk_file
    interactor.SetRenderWindow(renderer_window)
    interactor.Initialize()
    interactor.Start()

if __name__ == "__main__":

    carregarDiretoriasDataSets()
    carregarDataSets()
    binaryThresholdFun(dataSets[0], 2)
    writeItkImage(binaryThreshold.GetOutput())
    displayVtkFile(os.path.join(DiretoriaItkOutput, "output.vtk"))
