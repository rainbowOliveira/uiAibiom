import itk
import vtk
import os
from os import listdir
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


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

# ITK filters.
binaryThreshold = itk.BinaryThresholdImageFilter[ImageType, ImageType].New()

# VTK colours.
colors = vtk.vtkNamedColors()

# Initial Sagittal Slice.
sagittalSlice = 0
# Initial Coronal Slice.
coronalSlice = 0
# Initial Transverse Slice.
transverseSlice = 0

# Lista que armazena os itk datasets.
dataSets = []

# Itens selecionados pelo user.
dataset = 0
label = 0
plano = 0


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


def displayVtkFileSagittal(vtkDir):

    global vtkDims
    # VTK Image reader.
    vtkReader = vtk.vtkStructuredPointsReader()
    renderer = vtk.vtkRenderer()
    renderer_window = vtk.vtkRenderWindow()
    # VTK coronal sagittal widget.
    sagittal_widget = vtk.vtkImagePlaneWidget()
    # VTK isosurface
    iso = vtk.vtkMarchingCubes()
    # VTK renderer_window_interactor.
    interactor = vtk.vtkRenderWindowInteractor()
    # VTK mapper.
    mapper = vtk.vtkDataSetMapper()
    # VTK actor.
    actor = vtk.vtkActor()
    # VTK dataset dims.
    vtkDims = []

    vtkReader.SetFileName(vtkDir)
    vtkReader.Update()

    # Get the dims of the data
    vtkDims = vtkReader.GetOutput().GetDimensions()

    iso.SetInputConnection(vtkReader.GetOutputPort())
    iso.SetValue(0, 1)

    # Map the surface to graphics primitives
    mapper.SetInputConnection(iso.GetOutputPort())

    # Create an actor to represent the surface
    actor.SetMapper(mapper)

    renderer.SetBackground(0.1, 0.2, 0.4)

    # Define the rendering window
    renderer_window.AddRenderer(renderer)
    renderer_window.SetSize(800, 800)

    # Define the interactor
    interactor.SetRenderWindow(renderer_window)

    sagittal_widget.SetInteractor(interactor)
    sagittal_widget.RestrictPlaneToVolumeOn()
    sagittal_widget.SetInputConnection(vtkReader.GetOutputPort())
    sagittal_widget.SetPlaneOrientationToXAxes()
    sagittal_widget.SetSliceIndex(int(sagittalSlice))
    sagittal_widget.DisplayTextOn()
    sagittal_widget.SetDefaultRenderer(renderer)
    sagittal_widget.SetTexturePlaneProperty(actor.GetProperty())
    sagittal_widget.TextureInterpolateOff()
    sagittal_widget.SetPicker(None)
    sagittal_widget.On()

    # Bind the key press event to the interactor
    change_slice_sagittal_func = change_slice_sagittal(renderer_window, sagittal_widget)
    interactor.AddObserver(vtk.vtkCommand.KeyPressEvent, change_slice_sagittal_func)

    # Initialize the interactor and start the rendering loop
    renderer_window.Render()
    interactor.Start()

def displayVtkFileCoronal(vtkDir):

    global vtkDims
    # VTK Image reader.
    vtkReader = vtk.vtkStructuredPointsReader()
    renderer = vtk.vtkRenderer()
    renderer_window = vtk.vtkRenderWindow()
    # VTK coronal plan widget.
    coronal_widget = vtk.vtkImagePlaneWidget()
    # VTK isosurface
    iso = vtk.vtkMarchingCubes()
    # VTK renderer_window_interactor.
    interactor = vtk.vtkRenderWindowInteractor()
    # VTK mapper.
    mapper = vtk.vtkDataSetMapper()
    # VTK actor.
    actor = vtk.vtkActor()
    # VTK dataset dims.
    vtkDims = []

    vtkReader.SetFileName(vtkDir)
    vtkReader.Update()

    # Get the dims of the data
    vtkDims = vtkReader.GetOutput().GetDimensions()

    iso.SetInputConnection(vtkReader.GetOutputPort())
    iso.SetValue(0, 1)

    # Map the surface to graphics primitives
    mapper.SetInputConnection(iso.GetOutputPort())

    # Create an actor to represent the surface
    actor.SetMapper(mapper)

    renderer.SetBackground(0.1, 0.2, 0.4)

    # Define the rendering window
    renderer_window.AddRenderer(renderer)
    renderer_window.SetSize(800, 800)

    # Define the interactor
    interactor.SetRenderWindow(renderer_window)

    coronal_widget.SetInteractor(interactor)
    coronal_widget.RestrictPlaneToVolumeOn()
    coronal_widget.SetInputConnection(vtkReader.GetOutputPort())
    coronal_widget.SetPlaneOrientationToYAxes()
    coronal_widget.SetSliceIndex(int(coronalSlice))
    coronal_widget.DisplayTextOn()
    coronal_widget.SetDefaultRenderer(renderer)
    coronal_widget.SetTexturePlaneProperty(actor.GetProperty())
    coronal_widget.TextureInterpolateOff()
    coronal_widget.SetPicker(None)
    coronal_widget.On()

    # Bind the key press event to the interactor
    change_slice_coronal_func = change_slice_coronal(renderer_window, coronal_widget)
    interactor.AddObserver(vtk.vtkCommand.KeyPressEvent, change_slice_coronal_func)

    # Initialize the interactor and start the rendering loop
    renderer_window.Render()
    interactor.Start()

def displayVtkFileTransverse(vtkDir):

    global vtkDims
    # VTK Image reader.
    vtkReader = vtk.vtkStructuredPointsReader()
    renderer = vtk.vtkRenderer()
    renderer_window = vtk.vtkRenderWindow()
    # VTK transverse plan widget.
    transverse_widget = vtk.vtkImagePlaneWidget()
    # VTK isosurface
    iso = vtk.vtkMarchingCubes()
    # VTK renderer_window_interactor.
    interactor = vtk.vtkRenderWindowInteractor()
    # VTK mapper.
    mapper = vtk.vtkDataSetMapper()
    # VTK actor.
    actor = vtk.vtkActor()
    # VTK dataset dims.
    vtkDims = []

    vtkReader.SetFileName(vtkDir)
    vtkReader.Update()

    # Get the dims of the data
    vtkDims = vtkReader.GetOutput().GetDimensions()

    iso.SetInputConnection(vtkReader.GetOutputPort())
    iso.SetValue(0, 1)

    # Map the surface to graphics primitives
    mapper.SetInputConnection(iso.GetOutputPort())

    # Create an actor to represent the surface
    actor.SetMapper(mapper)

    renderer.SetBackground(0.1, 0.2, 0.4)

    # Define the rendering window
    renderer_window.AddRenderer(renderer)
    renderer_window.SetSize(800, 800)

    # Define the interactor
    interactor.SetRenderWindow(renderer_window)

    transverse_widget.SetInteractor(interactor)
    transverse_widget.RestrictPlaneToVolumeOn()
    transverse_widget.SetInputConnection(vtkReader.GetOutputPort())
    transverse_widget.SetPlaneOrientationToZAxes()
    transverse_widget.SetSliceIndex(int(transverseSlice))
    transverse_widget.DisplayTextOn()
    transverse_widget.SetDefaultRenderer(renderer)
    transverse_widget.SetTexturePlaneProperty(actor.GetProperty())
    transverse_widget.TextureInterpolateOff()
    transverse_widget.SetPicker(None)
    transverse_widget.On()

    # Bind the key press event to the interactor
    change_slice_transverse_func = change_slice_transverse(renderer_window, transverse_widget)
    interactor.AddObserver(vtk.vtkCommand.KeyPressEvent, change_slice_transverse_func)

    # Initialize the interactor and start the rendering loop
    renderer_window.Render()
    interactor.Start()

def change_slice_sagittal(renderer_window, sagittal_widget):
    def change_slice_sagittal_func(obj, event):
        global sagittalSlice
        global vtkDims

        key = obj.GetKeySym()

        if (key == "Right"):
            if (sagittalSlice < vtkDims[0]):
                sagittalSlice = sagittalSlice + 1
                sagittal_widget.SetSliceIndex(sagittalSlice)
                renderer_window.Render()
                print(key)

        else:
            if (key == "Left"):
                if (sagittalSlice > 0):
                    sagittalSlice = sagittalSlice - 1
                    sagittal_widget.SetSliceIndex(sagittalSlice)
                    renderer_window.Render()
                    print(key)
    return change_slice_sagittal_func

def change_slice_coronal(renderer_window, coronal_widget):
    def change_slice_coronal_func(obj, event):
        global coronalSlice
        global vtkDims

        key = obj.GetKeySym()

        if (key == "Right"):
            if (coronalSlice < vtkDims[1]):
                coronalSlice = coronalSlice + 1
                coronal_widget.SetSliceIndex(coronalSlice)
                renderer_window.Render()
                print(key)

        else:
            if (key == "Left"):
                if (coronalSlice > 0):
                    coronalSlice = coronalSlice - 1
                    coronal_widget.SetSliceIndex(coronalSlice)
                    renderer_window.Render()
                    print(key)
    return change_slice_coronal_func


def change_slice_transverse(renderer_window, transverse_widget):
    def change_slice_transverse_func(obj, event):
        global transverseSlice
        global vtkDims

        key = obj.GetKeySym()

        if (key == "Right"):
            if (transverseSlice < vtkDims[2]):
                transverseSlice = transverseSlice + 1
                transverse_widget.SetSliceIndex(transverseSlice)
                renderer_window.Render()
                print(key)

        else:
            if (key == "Left"):
                if (transverseSlice > 0):
                    transverseSlice = transverseSlice - 1
                    transverse_widget.SetSliceIndex(transverseSlice)
                    renderer_window.Render()
                    print(key)
    return change_slice_transverse_func

def menuPrincipal():

    i = 1

    print("\nMenu Principal - 1")

    for diretoriaDataset in DiretoriasDataSets:
        print(str(i) + "- " + os.path.basename(diretoriaDataset).split('/')[-1])
        i = i+1

    op = input("Escolha um dataset: ")

    return op


def menuLabel():

    print("\nMenu de Labeling - 2")
    print("1 - Cérebro")
    print("2 - Cerebelo")
    print("3 - Tronco Cerebral")
    print("4 - Corpo Caloso")
    print("5 - Fórnix")
    print("6 - Tálamus")
    print("7 - Mid Brain")
    print("8 - Pons")
    print("9 - Medula")
    print("10 - Ventrículos Laterais")
    print("11 - Terceiro Ventrículo")
    print("12 - Quarto Ventrículo")
    op = input("Selecione uma label: ")

    return op


def menuPlano():

    print("\nMenu de seleção do plano - 3")
    print("1 - Sagital")
    print("2 - Coronal")
    print("3 - Transversal")
    op = input("Selecione um plano: ")

    return op


if __name__ == "__main__":

    carregarDiretoriasDataSets()
    carregarDataSets()

    while True:

        dataset = int(menuPrincipal()) - 1
        label = int(menuLabel())
        plano = int(menuPlano())
        binaryThresholdFun(dataSets[dataset], label)
        writeItkImage(binaryThreshold.GetOutput())

        match plano:
            case 1:
                displayVtkFileSagittal(os.path.join(DiretoriaItkOutput, "output.vtk"))
            case 2:
                displayVtkFileCoronal(os.path.join(DiretoriaItkOutput, "output.vtk"))
            case 3:
                displayVtkFileTransverse(os.path.join(DiretoriaItkOutput, "output.vtk"))