import itk
import vtk
import os
from os import listdir
import sys
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# Estrutura do projeto.
project_dir = os.getcwd()
DiretoriaDataSets = os.path.join(project_dir, "DataSets")
DiretoriaItkOutput = os.path.join(project_dir, "ItkOutput")
DiretoriasDataSets = []

# ITK Image type.
Dimension = 3
# Pixel type.
PixelType = itk.US
ImageType = itk.Image[PixelType, Dimension]

# ITK Image writer.
writer = itk.ImageFileWriter[ImageType].New()

# VTK colours.
colors = vtk.vtkNamedColors()
# VTK renderer.
renderer = vtk.vtkRenderer()
# VTK sagittal widget.
sagittal_widget = vtk.vtkImagePlaneWidget()
# VTK coronal widget.
coronal_widget = vtk.vtkImagePlaneWidget()
# VTK transverse widget.
transverse_widget = vtk.vtkImagePlaneWidget()

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

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global renderer

        self.numDatasets = 0

        # Definem-se propriedades da window.
        self.setGeometry(300, 300, 400, 200)
        # Define-se o título da window.
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

        # Create radio buttons.
        self.buttonGroupDataset = QButtonGroup(self)
        self.buttonGroupLabel = QButtonGroup(self)
        self.buttonGroupPlane = QButtonGroup(self)

        self.rbLabel1 = QRadioButton('Cérebro', self)
        self.rbLabel1.setFont(QFont('Arial', 12))
        self.rbLabel2 = QRadioButton('Cerebelo', self)
        self.rbLabel2.setFont(QFont('Arial', 12))
        self.rbLabel3 = QRadioButton('Tronco Cerebral', self)
        self.rbLabel3.setFont(QFont('Arial', 12))
        self.rbLabel4 = QRadioButton('Corpo Caloso', self)
        self.rbLabel4.setFont(QFont('Arial', 12))
        self.rbLabel5 = QRadioButton('Fórnix', self)
        self.rbLabel5.setFont(QFont('Arial', 12))
        self.rbLabel6 = QRadioButton('Tálamus', self)
        self.rbLabel6.setFont(QFont('Arial', 12))
        self.rbLabel7 = QRadioButton('Mid Brain', self)
        self.rbLabel7.setFont(QFont('Arial', 12))
        self.rbLabel8 = QRadioButton('Pons', self)
        self.rbLabel8.setFont(QFont('Arial', 12))
        self.rbLabel9 = QRadioButton('Medula', self)
        self.rbLabel9.setFont(QFont('Arial', 12))
        self.rbLabel10 = QRadioButton('Ventrículos Laterais', self)
        self.rbLabel10.setFont(QFont('Arial', 12))
        self.rbLabel11 = QRadioButton('Terceiro Ventrículo', self)
        self.rbLabel11.setFont(QFont('Arial', 12))
        self.rbLabel12 = QRadioButton('Quarto Ventrículo', self)
        self.rbLabel12.setFont(QFont('Arial', 12))
        self.rbPlano1 = QRadioButton('Sagital', self)
        self.rbPlano1.setFont(QFont('Arial', 12))
        self.rbPlano2 = QRadioButton('Coronal', self)
        self.rbPlano2.setFont(QFont('Arial', 12))
        self.rbPlano3 = QRadioButton('Transversal', self)
        self.rbPlano3.setFont(QFont('Arial', 12))

        self.buttonGroupLabel.addButton(self.rbLabel1, 1)
        self.buttonGroupLabel.addButton(self.rbLabel2, 2)
        self.buttonGroupLabel.addButton(self.rbLabel3, 3)
        self.buttonGroupLabel.addButton(self.rbLabel4, 4)
        self.buttonGroupLabel.addButton(self.rbLabel5, 5)
        self.buttonGroupLabel.addButton(self.rbLabel6, 6)
        self.buttonGroupLabel.addButton(self.rbLabel7, 7)
        self.buttonGroupLabel.addButton(self.rbLabel8, 8)
        self.buttonGroupLabel.addButton(self.rbLabel9, 9)
        self.buttonGroupLabel.addButton(self.rbLabel10, 10)
        self.buttonGroupLabel.addButton(self.rbLabel11, 11)
        self.buttonGroupLabel.addButton(self.rbLabel12, 12)
        self.buttonGroupPlane.addButton(self.rbPlano1, 1)
        self.buttonGroupPlane.addButton(self.rbPlano2, 2)
        self.buttonGroupPlane.addButton(self.rbPlano3, 3)

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

        # Create dataset radiobuttons
        cont = 0
        for diretoriaDataset in DiretoriasDataSets:
            setattr(Window, f"attr_{'rbDataset' + str(cont + 1)}",
                    QRadioButton(os.path.basename(diretoriaDataset).split('/')[-1], self))
            rbDataset = getattr(Window, 'attr_rbDataset' + str(cont + 1))
            rbDataset.setFont(QFont('Arial', 12))
            self.buttonGroupDataset.addButton(rbDataset, cont + 1)
            vbox.addWidget(rbDataset)
            self.numDatasets = self.numDatasets + 1
            cont = cont + 1

        # Add check boxes to vbox.
        vbox.addLayout(label_layout1)
        vbox.addWidget(self.rbLabel1)
        vbox.addWidget(self.rbLabel2)
        vbox.addWidget(self.rbLabel3)
        vbox.addWidget(self.rbLabel4)
        vbox.addWidget(self.rbLabel5)
        vbox.addWidget(self.rbLabel6)
        vbox.addWidget(self.rbLabel7)
        vbox.addWidget(self.rbLabel8)
        vbox.addWidget(self.rbLabel9)
        vbox.addWidget(self.rbLabel10)
        vbox.addWidget(self.rbLabel11)
        vbox.addWidget(self.rbLabel12)
        vbox.addLayout(label_layout2)
        vbox.addWidget(self.rbPlano1)
        vbox.addWidget(self.rbPlano2)
        vbox.addWidget(self.rbPlano3)
        vbox.addWidget(submit_button)

        # Radio Buttons selecionados por padrão.
        self.attr_rbDataset1.setChecked(True)
        self.rbLabel1.setChecked(True)
        self.rbPlano1.setChecked(True)

        # Create a layout for the main window
        main_layout = QHBoxLayout()

        # Create VTK widget
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        vtk_layout = QVBoxLayout()
        vtk_layout.addWidget(self.vtkWidget)

        # Set size policy for VTK widget
        self.vtkWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.vtkWidget.setFixedSize(800, 600)

        # Add VTK widget to the main layout
        main_layout.addLayout(vtk_layout)

        # Add the vertical layout to the main layout
        main_layout.addLayout(vbox)

        # Set layout
        self.setLayout(main_layout)

        # Show window
        self.show()

    def submit(self):

        global dataset
        global label
        global plano
        global DiretoriasDataSets

        # Get checked dataset radio button
        btnDataset = self.buttonGroupDataset.checkedButton()
        if btnDataset is not None:
            dataset = self.buttonGroupDataset.checkedId() - 1
        else:
            dataset = None
            print('No dataset selected')

        # Get checked label radio button
        btnLabel = self.buttonGroupLabel.checkedButton()
        if btnLabel is not None:
            label = self.buttonGroupLabel.checkedId()
        else:
            label = None
            print('No label selected')

        # Get checked plane radio button
        btnPlane = self.buttonGroupPlane.checkedButton()
        if btnPlane is not None:
            plano = self.buttonGroupPlane.checkedId()
        else:
            plano = None
            print('No plan selected')

        if dataset is not None and label is not None:  # make sure both dataset and label are selected
            binaryThreshold = binaryThresholdFun(dataSets[dataset], label)
            volume = calculate_volume(binaryThreshold)
            writeItkImage(binaryThreshold.GetOutput())

            match plano:
                case 1:
                    displayVtkFileSagittal(renderer, os.path.join(DiretoriaItkOutput, "output.vtk"),
                                           DiretoriasDataSets[dataset],
                                           self.vtkWidget, volume)
                case 2:
                    displayVtkFileCoronal(renderer, os.path.join(DiretoriaItkOutput, "output.vtk"),
                                          DiretoriasDataSets[dataset],
                                          self.vtkWidget, volume)
                case 3:
                    displayVtkFileTransverse(renderer, os.path.join(DiretoriaItkOutput, "output.vtk"),
                                             DiretoriasDataSets[dataset],
                                             self.vtkWidget, volume)

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

def calculate_volume(binaryThreshold):
    # Convert the output image of the binaryThreshold filter to a NumPy array
    image_array = itk.array_from_image(binaryThreshold.GetOutput())

    # Count the number of voxels that are 1 (i.e., part of the structure)
    structure_voxels = np.count_nonzero(image_array)

    # Get the volume of a single voxel
    voxel_volume = np.prod(binaryThreshold.GetOutput().GetSpacing())

    # Calculate the volume of the structure
    structure_volume = structure_voxels * voxel_volume

    return structure_volume


def writeItkImage(itkImage):

    writer.SetInput(itkImage)
    writer.SetFileName(os.path.join(DiretoriaItkOutput, "output.vtk"))
    writer.Update()

def displayVtkFileSagittal(renderer, vtkDir, vtkDir1, vtkWidget, volume):
    # Corte sagital.
    global sagittalSlice
    global sagittal_widget
    sagittalSlice = 0

    # VTK Image reader.
    vtkReader1 = vtk.vtkStructuredPointsReader()
    # VTK renderer window.
    render_window = vtkWidget.GetRenderWindow()
    # VTK renderer_window_interactor.
    interactor = render_window.GetInteractor()

    renderer.RemoveAllViewProps()

    # Define-se o caminho até à imagem 'dataset.vtk'.
    vtkReader1.SetFileName(vtkDir1)
    # Carrega-se a imagem 'dataset.vtk'.
    vtkReader1.Update()

    # Aplicam-se os Outline e Contour Filter à imagem 'output.vtk'.
    actor1, actor2 = outLineAndContourFilters(vtkDir)

    # Criação do texto de anotação.
    text_actor = vtk.vtkTextActor()
    # Configuração do texto.
    text_actor.SetInput(f"Volume: {round(volume/1000, 1)} cm^3")
    # Configuração da cor do texto (branco).
    text_actor.GetTextProperty().SetColor(1, 1, 1)
    # Configuração da posição do texto na tela.
    text_actor.SetDisplayPosition(10, 10)

    # Define-se a cor do background da janela vtk.
    renderer.SetBackground(0.25, 0.25, 0.25)
    # Adiciona-se o actor OutLine à janela vtk.
    renderer.AddActor(actor1)
    # Adiciona-se o actor Contour à janela vtk.
    renderer.AddActor(actor2)
    # Adicionando o ator do texto ao renderizador.
    renderer.AddActor(text_actor)

    # Construção do renderizador da janela vtk.
    render_window.AddRenderer(renderer)
    interactor.RemoveObservers('RightButtonPressEvent')

    # Definem-se as interações do corte sagital.
    sagittal_widget.SetInteractor(interactor)
    # Define-se a imagem 'dataset.vtk' como input do widget corte sagital.
    sagittal_widget.SetInputConnection(vtkReader1.GetOutputPort())
    # Define-se a orientação do corte como sagital.
    sagittal_widget.SetPlaneOrientationToXAxes()
    # Define-se a posição inicial do corte sagital.
    sagittal_widget.SetSliceIndex(int(sagittalSlice))
    # Define-se a janela vtk do widget corte sagital.
    sagittal_widget.SetDefaultRenderer(renderer)
    # Disponibiliza-se o widget corte sagital.
    sagittal_widget.Off()
    sagittal_widget.On()

    # Vincula-se a 'change_slice_sagittal_func' ao evento de pressionar uma seta do teclado.
    change_slice_sagittal_func = change_slice_sagittal(render_window, sagittal_widget)
    render_window.GetInteractor().AddObserver(vtk.vtkCommand.KeyPressEvent, change_slice_sagittal_func)

    # Inicializam-se as interações e renderiza-se a janela vtk.
    interactor.Initialize()
    render_window.Render()
    interactor.Start()

def displayVtkFileCoronal(renderer, vtkDir, vtkDir1, vtkWidget, volume):
    # Corte coronal.
    global coronalSlice
    global coronal_widget
    coronalSlice = 0

    # VTK Image reader.
    vtkReader1 = vtk.vtkStructuredPointsReader()
    # VTK renderer window.
    render_window = vtkWidget.GetRenderWindow()
    # VTK renderer_window_interactor.
    interactor = render_window.GetInteractor()

    renderer.RemoveAllViewProps()

    # Define-se o caminho até à imagem 'dataset.vtk'.
    vtkReader1.SetFileName(vtkDir1)
    # Carrega-se a imagem 'dataset.vtk'.
    vtkReader1.Update()

    # Aplicam-se os Outline e Contour Filter à imagem 'output.vtk'.
    actor1, actor2 = outLineAndContourFilters(vtkDir)

    # Criação do texto de anotação.
    text_actor = vtk.vtkTextActor()
    # Configuração do texto.
    text_actor.SetInput(f"Volume: {round(volume/1000, 1)} cm^3")
    # Configuração da cor do texto (branco).
    text_actor.GetTextProperty().SetColor(1, 1, 1)
    # Configuração da posição do texto na tela.
    text_actor.SetDisplayPosition(10, 10)

    # Define-se a cor do background da janela vtk.
    renderer.SetBackground(0.25, 0.25, 0.25)
    # Adiciona-se o actor OutLine à janela vtk.
    renderer.AddActor(actor1)
    # Adiciona-se o actor Contour à janela vtk.
    renderer.AddActor(actor2)
    # Adicionando o ator do texto ao renderizador.
    renderer.AddActor(text_actor)

    # Construção do renderizador da janela vtk.
    render_window.AddRenderer(renderer)
    interactor.RemoveObservers('RightButtonPressEvent')

    # Definem-se as interações do corte coronal.
    coronal_widget.SetInteractor(interactor)
    # Define-se a imagem 'dataset.vtk' como input do widget corte coronal.
    coronal_widget.SetInputConnection(vtkReader1.GetOutputPort())
    # Define-se a orientação do corte como coronal.
    coronal_widget.SetPlaneOrientationToYAxes()
    # Define-se a posição inicial do corte coronal.
    coronal_widget.SetSliceIndex(int(coronalSlice))
    # Define-se a janela vtk do widget corte coronal.
    coronal_widget.SetDefaultRenderer(renderer)
    # Disponibiliza-se o widget corte coronal.
    coronal_widget.Off()
    coronal_widget.On()

    # Vincula-se a 'change_slice_coronal_func' ao evento de pressionar uma seta do teclado.
    change_slice_coronal_func = change_slice_coronal(render_window, coronal_widget)
    interactor.AddObserver(vtk.vtkCommand.KeyPressEvent, change_slice_coronal_func)

    # Inicializam-se as interações e renderiza-se a janela vtk.
    interactor.Initialize()
    render_window.Render()
    interactor.Start()

def displayVtkFileTransverse(renderer, vtkDir, vtkDir1, vtkWidget, volume):
    # Corte transversal.
    global transverseSlice
    global transverse_widget
    transverseSlice = 0

    # VTK Image reader.
    vtkReader1 = vtk.vtkStructuredPointsReader()
    # VTK renderer window.
    render_window = vtkWidget.GetRenderWindow()
    # VTK renderer_window_interactor.
    interactor = render_window.GetInteractor()

    renderer.RemoveAllViewProps()

    # Define-se o caminho até à imagem 'dataset.vtk'.
    vtkReader1.SetFileName(vtkDir1)
    # Carrega-se a imagem 'dataset.vtk'.
    vtkReader1.Update()

    # Aplicam-se os Outline e Contour Filter à imagem 'output.vtk'.
    actor1, actor2 = outLineAndContourFilters(vtkDir)

    # Criação do texto de anotação.
    text_actor = vtk.vtkTextActor()
    # Configuração do texto.
    text_actor.SetInput(f"Volume: {round(volume/1000, 1)} cm^3")
    # Configuração da cor do texto (branco).
    text_actor.GetTextProperty().SetColor(1, 1, 1)
    # Configuração da posição do texto na tela.
    text_actor.SetDisplayPosition(10, 10)

    # Define-se a cor do background da janela vtk.
    renderer.SetBackground(0.25, 0.25, 0.25)
    # Adiciona-se o actor OutLine à janela vtk.
    renderer.AddActor(actor1)
    # Adiciona-se o actor Contour à janela vtk.
    renderer.AddActor(actor2)
    # Adicionando o ator do texto ao renderizador.
    renderer.AddActor(text_actor)

    # Construção do renderizador da janela vtk.
    render_window.AddRenderer(renderer)
    interactor.RemoveObservers('RightButtonPressEvent')

    # Definem-se as interações do corte transversal.
    transverse_widget.SetInteractor(interactor)
    # Define-se a imagem 'dataset.vtk' como input do widget corte transversal.
    transverse_widget.SetInputConnection(vtkReader1.GetOutputPort())
    # Define-se a orientação do corte como transversal.
    transverse_widget.SetPlaneOrientationToZAxes()
    # Define-se a posição inicial do corte transversal.
    transverse_widget.SetSliceIndex(int(transverseSlice))
    # Define-se a janela vtk do widget corte transversal.
    transverse_widget.SetDefaultRenderer(renderer)
    # Disponibiliza-se o widget corte transversal.
    transverse_widget.Off()
    transverse_widget.On()

    # Vincula-se a 'change_slice_transverse_func' ao evento de pressionar uma seta do teclado.
    change_slice_transverse_func = change_slice_transverse(render_window, transverse_widget)
    interactor.AddObserver(vtk.vtkCommand.KeyPressEvent, change_slice_transverse_func)

    # Inicializam-se as interações e renderiza-se a janela vtk.
    interactor.Initialize()
    render_window.Render()
    interactor.Start()

def outLineAndContourFilters(vtkDir):
    # Número de cortes sagitais, coronais e transversais.
    global vtkDims

    # VTK Image reader.
    vtkReader = vtk.vtkStructuredPointsReader()

    # Define-se o caminho até à imagem 'output.vtk'.
    vtkReader.SetFileName(vtkDir)
    # Carrega-se a imagem output.vtk.
    vtkReader.Update()

    # Obtêm-se o número de cortes sagitais, coronais e transversais.
    vtkDims = vtkReader.GetOutput().GetDimensions()

    # Inicializa-se o Outline Filter.
    outlineFilter = vtk.vtkOutlineFilter()
    # Define-se a imagem 'output.vtk' como input do Outline Filter.
    outlineFilter.SetInputData(vtkReader.GetOutput())
    # Processa-se a imagem ´output.vtk´ com o OutLine Filter.
    outlineFilter.Update()

    # Obtêm-se o output do OutLine Filter.
    outline = outlineFilter.GetOutput()

    # Inicializa-se o Contour Filter.
    contourFilter = vtk.vtkContourFilter()
    # Definem-se parâmetros do Contour Filter.
    isovalue = 0.5
    contourFilter.SetValue(0, isovalue)
    # Define-se a imagem ´output.vtk´ como input do Contour Filter.
    contourFilter.SetInputData(vtkReader.GetOutput())
    # Processa-se a imagem 'output.vtk' com o Contour Filter.
    contourFilter.Update()

    # Obtêm-se o output do Contour Filter.
    isosurface = contourFilter.GetOutput()

    # Inicializa-se o mapper do OutLine Filter.
    mapper1 = vtk.vtkPolyDataMapper()
    # Construção do OutLine mapper a partir do output do OutLine Filter.
    mapper1.SetInputData(outline)

    # Inicializa-se o mapper do Contour Filter.
    mapper2 = vtk.vtkPolyDataMapper()
    # Contrução do Contour mapper a partir do output do Contour Filter.
    mapper2.SetInputData(isosurface)

    # Inicializa-se o actor OutLine.
    actor1 = vtk.vtkActor()
    # Contrução do actor OutLine através do OutLine mapper.
    actor1.SetMapper(mapper1)
    # Define-se a cor do actor OutLine.
    actor1.GetProperty().SetColor(1, 1, 1)
    # Define-se a opacidade do actor OutLine.
    actor1.GetProperty().SetOpacity(0.5)

    # Inicializa-se o actor Contour.
    actor2 = vtk.vtkActor()
    # Contrução do actor Contour através do Contour mapper.
    actor2.SetMapper(mapper2)
    # Define-se a cor do actor Contour.
    actor2.GetProperty().SetColor(1, 1, 0)  # RGB
    # Define-se a opacidade do actor Contour.
    actor2.GetProperty().SetOpacity(1)

    # Retornam-se os actores dos filtros aplicados.
    return actor1, actor2

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

        else:
            if (key == "Left"):
                if (sagittalSlice > 0):
                    sagittalSlice = sagittalSlice - 1
                    sagittal_widget.SetSliceIndex(sagittalSlice)
                    renderer_window.Render()
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

        else:
            if (key == "Left"):
                if (coronalSlice > 0):
                    coronalSlice = coronalSlice - 1
                    coronal_widget.SetSliceIndex(coronalSlice)
                    renderer_window.Render()
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

        else:
            if (key == "Left"):
                if (transverseSlice > 0):
                    transverseSlice = transverseSlice - 1
                    transverse_widget.SetSliceIndex(transverseSlice)
                    renderer_window.Render()
    return change_slice_transverse_func

if __name__ == "__main__":

    carregarDiretoriasDataSets()
    carregarDataSets()

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())