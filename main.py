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

# ITK Image writer.
writer = itk.ImageFileWriter[ImageType].New()

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
dataset = None
label = None
plano = None


def carregarDiretoriasDataSets():
    # Carregam-se as diretorias de todos os datasets.
    for diretoriaDataSet in listdir(DiretoriaDataSets):
        DiretoriasDataSets.append(os.path.join(DiretoriaDataSets, diretoriaDataSet))
    print(DiretoriasDataSets)


def carregarDataSets():
    # Carregam-se todos os datasets.
    for diretoriaDataSet in DiretoriasDataSets:
        itkReader = itk.ImageFileReader[ImageType].New()
        itkReader.SetFileName(diretoriaDataSet)
        itkReader.Update()
        dataSets.append(itkReader.GetOutput())
    print(dataSets)


def binaryThresholdFun(itkImage, label):
    outsideValue = 0
    insideValue = 1

    # ITK filters.
    binaryThreshold = itk.BinaryThresholdImageFilter[ImageType, ImageType].New()
    binaryThreshold.SetLowerThreshold(label)
    binaryThreshold.SetUpperThreshold(label)
    binaryThreshold.SetOutsideValue(outsideValue)
    binaryThreshold.SetInsideValue(insideValue)
    binaryThreshold.SetInput(itkImage)
    binaryThreshold.Update()

    return binaryThreshold


def writeItkImage(itkImage):
    writer.SetInput(itkImage)
    writer.SetFileName(os.path.join(DiretoriaItkOutput, "output.vtk"))
    writer.Update()


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.numDatasets = 0

        # Set window properties
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Análise de imagem biomédica')

        self.title = QLabel('Análise de imagem biomédica', self)
        self.title.setFont(QFont('Arial', 30))

        # Set window background color
        self.setStyleSheet("background-color: #f0f0f0;")

        # Create labels
        self.label = QLabel('Selecione o dataset:', self)
        self.label.setFont(QFont('Arial', 16))
        self.label.setStyleSheet("color: #ffffff; background-color: #333333; font-size: 16pt;")
        self.label1 = QLabel('Selecione a label:', self)
        self.label1.setFont(QFont('Arial', 16))
        self.label1.setStyleSheet("color: #ffffff; background-color: #333333; font-size: 16pt;")
        self.label2 = QLabel('Selecione o plano:', self)
        self.label2.setFont(QFont('Arial', 16))
        self.label2.setStyleSheet("color: #ffffff; background-color: #333333; font-size: 16pt;")

        self.cbLabel1 = QCheckBox('Cérebro', self)
        self.cbLabel1.setFont(QFont('Arial', 12))
        self.cbLabel2 = QCheckBox('Cerebelo', self)
        self.cbLabel2.setFont(QFont('Arial', 12))
        self.cbLabel3 = QCheckBox('Tronco Cerebral', self)
        self.cbLabel3.setFont(QFont('Arial', 12))
        self.cbLabel4 = QCheckBox('Corpo Caloso', self)
        self.cbLabel4.setFont(QFont('Arial', 12))
        self.cbLabel5 = QCheckBox('Fórnix', self)
        self.cbLabel5.setFont(QFont('Arial', 12))
        self.cbLabel6 = QCheckBox('Tálamus', self)
        self.cbLabel6.setFont(QFont('Arial', 12))
        self.cbLabel7 = QCheckBox('Mid Brain', self)
        self.cbLabel7.setFont(QFont('Arial', 12))
        self.cbLabel8 = QCheckBox('Pons', self)
        self.cbLabel8.setFont(QFont('Arial', 12))
        self.cbLabel9 = QCheckBox('Medula', self)
        self.cbLabel9.setFont(QFont('Arial', 12))
        self.cbLabel10 = QCheckBox('Ventrículos Laterais', self)
        self.cbLabel10.setFont(QFont('Arial', 12))
        self.cbLabel11 = QCheckBox('Terceiro Ventrículo', self)
        self.cbLabel11.setFont(QFont('Arial', 12))
        self.cbLabel12 = QCheckBox('Quarto Ventrículo', self)
        self.cbLabel12.setFont(QFont('Arial', 12))
        self.cbPlano1 = QCheckBox('Sagital', self)
        self.cbPlano1.setFont(QFont('Arial', 12))
        self.cbPlano2 = QCheckBox('Coronal', self)
        self.cbPlano2.setFont(QFont('Arial', 12))
        self.cbPlano3 = QCheckBox('Transversal', self)
        self.cbPlano3.setFont(QFont('Arial', 12))

        # Create submit button
        submit_button = QPushButton('Submit', self)
        submit_button.setFont(QFont('Arial', 12))
        submit_button.setGeometry(QRect(140, 150, 120, 40))
        submit_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; font-size: 30px;")
        submit_button.clicked.connect(self.submit)

        # Create horizontal layout for labels
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title)
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.label)
        label_layout1 = QHBoxLayout()
        label_layout1.addWidget(self.label1)
        label_layout2 = QHBoxLayout()
        label_layout2.addWidget(self.label2)

        # Create vertical layout for checkboxes, labels and submit button
        vbox = QVBoxLayout()
        vbox.addLayout(title_layout)
        vbox.addLayout(label_layout)

        cont = 0
        for diretoriaDataset in DiretoriasDataSets:
            setattr(Window, f"attr_{'cbDataset' + str(cont + 1)}",
                    QRadioButton(os.path.basename(diretoriaDataset).split('/')[-1], self))
            cbDataset = getattr(Window, 'attr_cbDataset' + str(cont + 1))
            cbDataset.setFont(QFont('Arial', 12))
            vbox.addWidget(cbDataset)
            self.numDatasets = self.numDatasets + 1
            cont = cont + 1


        vbox.addLayout(label_layout1)
        vbox.addWidget(self.cbLabel1)
        vbox.addWidget(self.cbLabel2)
        vbox.addWidget(self.cbLabel3)
        vbox.addWidget(self.cbLabel4)
        vbox.addWidget(self.cbLabel5)
        vbox.addWidget(self.cbLabel6)
        vbox.addWidget(self.cbLabel7)
        vbox.addWidget(self.cbLabel8)
        vbox.addWidget(self.cbLabel9)
        vbox.addWidget(self.cbLabel10)
        vbox.addWidget(self.cbLabel11)
        vbox.addWidget(self.cbLabel12)
        vbox.addLayout(label_layout2)
        vbox.addWidget(self.cbPlano1)
        vbox.addWidget(self.cbPlano2)
        vbox.addWidget(self.cbPlano3)
        vbox.addWidget(submit_button)

        # Add vertical layout to grid layout
        grid = QGridLayout()
        grid.addLayout(vbox, 0, 0)

        # Set stretch factor for row and column that contains the label
        grid.setColumnStretch(0, 1)
        grid.setRowStretch(1, 1)

        # Set layout
        self.setLayout(grid)

        # Show window
        self.show()

    def submit(self):
        global dataset
        global label
        global plano
        global DiretoriasDataSets
        aux = 0

        for cont in range(self.numDatasets):
            cbDataset = getattr(Window, 'attr_cbDataset' + str(cont + 1))
            if cbDataset.isChecked():
                dataset = cont
                aux = aux + 1
        if aux == 0:
            dataset = None
            print('No dataset selected')

        if self.cbLabel1.isChecked():
            label = 1
        elif self.cbLabel2.isChecked():
            label = 2
        elif self.cbLabel3.isChecked():
            label = 3
        elif self.cbLabel4.isChecked():
            label = 4
        elif self.cbLabel5.isChecked():
            label = 5
        elif self.cbLabel6.isChecked():
            label = 6
        elif self.cbLabel7.isChecked():
            label = 7
        elif self.cbLabel8.isChecked():
            label = 8
        elif self.cbLabel9.isChecked():
            label = 9
        elif self.cbLabel10.isChecked():
            label = 10
        elif self.cbLabel11.isChecked():
            label = 11
        elif self.cbLabel12.isChecked():
            label = 12
        else:
            label = None
            print('No label selected')

        if self.cbPlano1.isChecked():
            plano = 1
        elif self.cbPlano2.isChecked():
            plano = 2
        elif self.cbPlano3.isChecked():
            plano = 3
        else:
            plano = None
            print('No plan selected')

        binaryThreshold = binaryThresholdFun(dataSets[dataset], label)
        writeItkImage(binaryThreshold.GetOutput())

        match plano:
            case 1:
                displayVtkFileSagittal(os.path.join(DiretoriaItkOutput, "output.vtk"), DiretoriasDataSets[dataset])
            case 2:
                displayVtkFileCoronal(os.path.join(DiretoriaItkOutput, "output.vtk"), DiretoriasDataSets[dataset])
            case 3:
                displayVtkFileTransverse(os.path.join(DiretoriaItkOutput, "output.vtk"), DiretoriasDataSets[dataset])


def displayVtkFileSagittal(vtkDir, vtkDir1):
    global vtkDims

    # VTK Image reader.
    vtkReader = vtk.vtkStructuredPointsReader()
    # VTK Image reader.
    vtkReader1 = vtk.vtkStructuredPointsReader()
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

    vtkReader.SetFileName(vtkDir)
    vtkReader.Update()
    vtkReader1.SetFileName(vtkDir1)
    vtkReader1.Update()

    # Get the dims of the data
    vtkDims = vtkReader.GetOutput().GetDimensions()

    outlineFilter = vtk.vtkOutlineFilter()
    outlineFilter.SetInputData(vtkReader.GetOutput())
    outlineFilter.Update()

    outline = outlineFilter.GetOutput()

    isovalue = 0.5
    contourFilter = vtk.vtkContourFilter()
    contourFilter.SetValue(0, isovalue)
    contourFilter.SetInputData(vtkReader.GetOutput())
    contourFilter.Update()

    isosurface = contourFilter.GetOutput()

    mapper1 = vtk.vtkPolyDataMapper()
    mapper1.SetInputData(outline)
    mapper1.ScalarVisibilityOff()

    mapper2 = vtk.vtkPolyDataMapper()
    mapper2.SetInputData(isosurface)
    mapper2.ScalarVisibilityOff()

    actor1 = vtk.vtkActor()
    actor1.SetMapper(mapper1)
    actor1.GetProperty().SetColor(1, 1, 1)  # RGB
    actor1.GetProperty().SetOpacity(0.5)

    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)
    actor2.GetProperty().SetColor(1, 1, 0)  # RGB
    actor2.GetProperty().SetOpacity(1)

    iso.SetInputConnection(vtkReader.GetOutputPort())
    iso.SetValue(0, 1)

    # Map the surface to graphics primitives
    mapper.SetInputConnection(iso.GetOutputPort())

    # Create an actor to represent the surface
    actor.SetMapper(mapper)

    renderer.SetBackground(0.25, 0.25, 0.25)
    renderer.AddActor(actor)
    renderer.AddActor(actor1)
    renderer.AddActor(actor2)

    # Define the rendering window
    renderer_window.AddRenderer(renderer)
    renderer_window.SetSize(800, 800)

    # Define the interactor
    interactor.SetRenderWindow(renderer_window)

    sagittal_widget.SetInteractor(interactor)
    sagittal_widget.RestrictPlaneToVolumeOn()
    sagittal_widget.SetInputConnection(vtkReader1.GetOutputPort())
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


def displayVtkFileCoronal(vtkDir, vtkDir1):
    global vtkDims
    # VTK Image reader.
    vtkReader = vtk.vtkStructuredPointsReader()
    # VTK Image reader.
    vtkReader1 = vtk.vtkStructuredPointsReader()
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

    vtkReader.SetFileName(vtkDir)
    vtkReader.Update()
    vtkReader1.SetFileName(vtkDir1)
    vtkReader1.Update()

    # Get the dims of the data
    vtkDims = vtkReader.GetOutput().GetDimensions()

    outlineFilter = vtk.vtkOutlineFilter()
    outlineFilter.SetInputData(vtkReader.GetOutput())
    outlineFilter.Update()

    outline = outlineFilter.GetOutput()

    isovalue = 0.5
    contourFilter = vtk.vtkContourFilter()
    contourFilter.SetValue(0, isovalue)
    contourFilter.SetInputData(vtkReader.GetOutput())
    contourFilter.Update()

    isosurface = contourFilter.GetOutput()

    mapper1 = vtk.vtkPolyDataMapper()
    mapper1.SetInputData(outline)
    mapper1.ScalarVisibilityOff()

    mapper2 = vtk.vtkPolyDataMapper()
    mapper2.SetInputData(isosurface)
    mapper2.ScalarVisibilityOff()

    actor1 = vtk.vtkActor()
    actor1.SetMapper(mapper1)
    actor1.GetProperty().SetColor(1, 1, 1)  # RGB
    actor1.GetProperty().SetOpacity(0.5)

    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)
    actor2.GetProperty().SetColor(1, 1, 0)  # RGB
    actor2.GetProperty().SetOpacity(1)

    iso.SetInputConnection(vtkReader.GetOutputPort())
    iso.SetValue(0, 1)

    # Map the surface to graphics primitives
    mapper.SetInputConnection(iso.GetOutputPort())

    # Create an actor to represent the surface
    actor.SetMapper(mapper)

    renderer.SetBackground(0.1, 0.2, 0.4)
    renderer.AddActor(actor)
    renderer.AddActor(actor1)
    renderer.AddActor(actor2)

    # Define the rendering window
    renderer_window.AddRenderer(renderer)
    renderer_window.SetSize(800, 800)

    # Define the interactor
    interactor.SetRenderWindow(renderer_window)

    coronal_widget.SetInteractor(interactor)
    coronal_widget.RestrictPlaneToVolumeOn()
    coronal_widget.SetInputConnection(vtkReader1.GetOutputPort())
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


def displayVtkFileTransverse(vtkDir, vtkDir1):
    global vtkDims
    # VTK Image reader.
    vtkReader = vtk.vtkStructuredPointsReader()
    vtkReader1 = vtk.vtkStructuredPointsReader()
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

    vtkReader.SetFileName(vtkDir)
    vtkReader.Update()
    vtkReader1.SetFileName(vtkDir1)
    vtkReader1.Update()

    # Get the dims of the data
    vtkDims = vtkReader.GetOutput().GetDimensions()

    outlineFilter = vtk.vtkOutlineFilter()
    outlineFilter.SetInputData(vtkReader.GetOutput())
    outlineFilter.Update()

    outline = outlineFilter.GetOutput()

    isovalue = 0.5
    contourFilter = vtk.vtkContourFilter()
    contourFilter.SetValue(0, isovalue)
    contourFilter.SetInputData(vtkReader.GetOutput())
    contourFilter.Update()

    isosurface = contourFilter.GetOutput()

    mapper1 = vtk.vtkPolyDataMapper()
    mapper1.SetInputData(outline)
    mapper1.ScalarVisibilityOff()

    mapper2 = vtk.vtkPolyDataMapper()
    mapper2.SetInputData(isosurface)
    mapper2.ScalarVisibilityOff()

    actor1 = vtk.vtkActor()
    actor1.SetMapper(mapper1)
    actor1.GetProperty().SetColor(1, 1, 1)  # RGB
    actor1.GetProperty().SetOpacity(0.5)

    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)
    actor2.GetProperty().SetColor(1, 1, 0)  # RGB
    actor2.GetProperty().SetOpacity(1)

    iso.SetInputConnection(vtkReader.GetOutputPort())
    iso.SetValue(0, 1)

    # Map the surface to graphics primitives
    mapper.SetInputConnection(iso.GetOutputPort())

    # Create an actor to represent the surface
    actor.SetMapper(mapper)

    renderer.SetBackground(0.1, 0.2, 0.4)
    renderer.AddActor(actor)
    renderer.AddActor(actor1)
    renderer.AddActor(actor2)

    # Define the rendering window
    renderer_window.AddRenderer(renderer)
    renderer_window.SetSize(800, 800)

    # Define the interactor
    interactor.SetRenderWindow(renderer_window)

    transverse_widget.SetInteractor(interactor)
    transverse_widget.RestrictPlaneToVolumeOn()
    transverse_widget.SetInputConnection(vtkReader1.GetOutputPort())
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
                if coronalSlice > 0:
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


if __name__ == "__main__":
    carregarDiretoriasDataSets()
    carregarDataSets()

    app = QApplication(sys.argv)

    # Open the style sheet file and read it
    with open('style.qss', 'r') as f:
        style = f.read()
    # Set the current style sheet
    app.setStyleSheet(style)

    ex = Window()
    sys.exit(app.exec_())
