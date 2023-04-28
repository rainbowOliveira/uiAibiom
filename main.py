import itk
import vtk
import os
from os import listdir

# ITK Image type.
Dimension = 3
PixelType = itk.US
ImageType = itk.Image[PixelType, Dimension]

# ITK Image reader.
reader = itk.ImageFileReader[ImageType].New()
# VTK Image reader.
reader1 = vtk.vtkDataSetReader()

diretoriasDataSets = []
dataSets = []

def carregarDiretoriasDataSets():

    project_dir = os.getcwd()
    diretoriaDataSets = os.path.join(project_dir, "DataSets")
    # Carregam-se as diretorias de todos os datasets.
    for diretoriaDataSet in listdir(diretoriaDataSets):
        diretoriasDataSets.append(os.path.join(diretoriaDataSets, diretoriaDataSet))
    print(diretoriasDataSets)

def carregarDataSets():

    # Carregam-se todos os datasets.
    for diretoriaDataSet in diretoriasDataSets:
        reader.SetFileName(diretoriaDataSet)
        reader.Update()
        dataSets.append(reader.GetOutput())
    print(dataSets)

def displayVtkFile(vtkDir):

    colors = vtk.vtkNamedColors()

    # Read the source file.
    reader1.SetFileName(vtkDir)
    reader1.ReadAllScalarsOn()  # Activate the reading of all scalars
    reader1.ReadAllVectorsOn()  # Activate the reading of all vectors
    reader1.ReadAllTensorsOn()  # Activate the reading of all tensors
    reader1.Update()  # Needed because of GetScalarRange
    output = reader1.GetOutput()
    scalar_range = output.GetScalarRange()

    # Create the mapper that corresponds the objects of the vtk.vtk file
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(output)
    mapper.SetScalarRange(scalar_range)
    # mapper.ScalarVisibilityOff()

    # Create the Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().SetLineWidth(2.0)
    actor.GetProperty().SetColor(colors.GetColor3d("MistyRose"))

    backface = vtk.vtkProperty()
    backface.SetColor(colors.GetColor3d('Tomato'))
    actor.SetBackfaceProperty(backface)

    # Create the Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('Wheat'))

    # Create the RendererWindow
    renderer_window = vtk.vtkRenderWindow()
    renderer_window.SetSize(640, 480)
    renderer_window.AddRenderer(renderer)
    renderer_window.SetWindowName('ReadVtkFile')

    # Create the RendererWindowInteractor and display the vtk_file
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderer_window)
    interactor.Initialize()
    interactor.Start()

if __name__ == "__main__":

    carregarDiretoriasDataSets()
    carregarDataSets()
    displayVtkFile(diretoriasDataSets[0])
