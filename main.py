import itk
import vtk
import os
from os import listdir
import sys
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
            setattr(Window, f"attr_{'cbDataset' + str(cont+1)}", QCheckBox(os.path.basename(diretoriaDataset).split('/')[-1], self))
            cbDataset = getattr(Window, 'attr_cbDataset' + str(cont+1))
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
                displayVtkFileSagittal(renderer, os.path.join(DiretoriaItkOutput, "output.vtk"), DiretoriasDataSets[dataset],
                                       self.vtkWidget)
            case 2:
                displayVtkFileCoronal(renderer, os.path.join(DiretoriaItkOutput, "output.vtk"), DiretoriasDataSets[dataset],
                                      self.vtkWidget)
            case 3:
                displayVtkFileTransverse(renderer, os.path.join(DiretoriaItkOutput, "output.vtk"), DiretoriasDataSets[dataset],
                                         self.vtkWidget)

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

def displayVtkFileSagittal(renderer, vtkDir, vtkDir1, vtkWidget):
    # Corte sagital.
    global sagittalSlice
    sagittalSlice = 0

    # VTK Image reader.
    vtkReader1 = vtk.vtkStructuredPointsReader()
    # VTK renderer window.
    render_window = vtkWidget.GetRenderWindow()
    # VTK coronal sagittal widget.
    sagittal_widget = vtk.vtkImagePlaneWidget()
    # VTK renderer_window_interactor.
    interactor = render_window.GetInteractor()

    renderer.RemoveAllViewProps()

    # Define-se o caminho até à imagem 'dataset.vtk'.
    vtkReader1.SetFileName(vtkDir1)
    # Carrega-se a imagem 'dataset.vtk'.
    vtkReader1.Update()

    # Aplicam-se os Outline e Contour Filter à imagem 'output.vtk'.
    actor1, actor2 = outLineAndContourFilters(vtkDir)

    # Define-se a cor do background da janela vtk.
    renderer.SetBackground(0.25, 0.25, 0.25)
    # Adiciona-se o actor OutLine à janela vtk.
    renderer.AddActor(actor1)
    # Adiciona-se o actor Contour à janela vtk.
    renderer.AddActor(actor2)

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
    sagittal_widget.On()

    # Vincula-se a 'change_slice_sagittal_func' ao evento de pressionar uma seta do teclado.
    change_slice_sagittal_func = change_slice_sagittal(render_window, sagittal_widget)
    render_window.GetInteractor().AddObserver(vtk.vtkCommand.KeyPressEvent, change_slice_sagittal_func)

    # Inicializam-se as interações e renderiza-se a janela vtk.
    interactor.Initialize()
    render_window.Render()
    interactor.Start()

def displayVtkFileCoronal(renderer, vtkDir, vtkDir1, vtkWidget):
    # Corte coronal.
    global coronalSlice
    coronalSlice = 0

    # VTK Image reader.
    vtkReader1 = vtk.vtkStructuredPointsReader()
    # VTK renderer window.
    render_window = vtkWidget.GetRenderWindow()
    # VTK coronal sagittal widget.
    coronal_widget = vtk.vtkImagePlaneWidget()
    # VTK renderer_window_interactor.
    interactor = render_window.GetInteractor()

    renderer.RemoveAllViewProps()

    # Define-se o caminho até à imagem 'dataset.vtk'.
    vtkReader1.SetFileName(vtkDir1)
    # Carrega-se a imagem 'dataset.vtk'.
    vtkReader1.Update()

    # Aplicam-se os Outline e Contour Filter à imagem 'output.vtk'.
    actor1, actor2 = outLineAndContourFilters(vtkDir)

    # Define-se a cor do background da janela vtk.
    renderer.SetBackground(0.25, 0.25, 0.25)
    # Adiciona-se o actor OutLine à janela vtk.
    renderer.AddActor(actor1)
    # Adiciona-se o actor Contour à janela vtk.
    renderer.AddActor(actor2)

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
    coronal_widget.On()

    # Vincula-se a 'change_slice_coronal_func' ao evento de pressionar uma seta do teclado.
    change_slice_coronal_func = change_slice_coronal(render_window, coronal_widget)
    interactor.AddObserver(vtk.vtkCommand.KeyPressEvent, change_slice_coronal_func)

    # Inicializam-se as interações e renderiza-se a janela vtk.
    interactor.Initialize()
    render_window.Render()
    interactor.Start()

def displayVtkFileTransverse(renderer, vtkDir, vtkDir1, vtkWidget):
    # Corte transversal.
    global transverseSlice
    transverseSlice = 0

    # VTK Image reader.
    vtkReader1 = vtk.vtkStructuredPointsReader()
    # VTK renderer window.
    render_window = vtkWidget.GetRenderWindow()
    # VTK coronal sagittal widget.
    transverse_widget = vtk.vtkImagePlaneWidget()
    # VTK renderer_window_interactor.
    interactor = render_window.GetInteractor()

    renderer.RemoveAllViewProps()

    # Define-se o caminho até à imagem 'dataset.vtk'.
    vtkReader1.SetFileName(vtkDir1)
    # Carrega-se a imagem 'dataset.vtk'.
    vtkReader1.Update()

    # Aplicam-se os Outline e Contour Filter à imagem 'output.vtk'.
    actor1, actor2 = outLineAndContourFilters(vtkDir)

    # Define-se a cor do background da janela vtk.
    renderer.SetBackground(0.25, 0.25, 0.25)
    # Adiciona-se o actor OutLine à janela vtk.
    renderer.AddActor(actor1)
    # Adiciona-se o actor Contour à janela vtk.
    renderer.AddActor(actor2)

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

if __name__ == "__main__":

    carregarDiretoriasDataSets()
    carregarDataSets()

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())