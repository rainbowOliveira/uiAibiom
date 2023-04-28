import itk
import os
from os import listdir

# Obtêm-se a diretoria onde se encontram todos os datasets.
project_dir = os.getcwd()
diretoriaDataSets = os.path.join(project_dir, "DataSets")

# ITK Image type.
Dimension = 3
PixelType = itk.US
ImageType = itk.Image[PixelType, Dimension]

# ITK Image reader.
reader = itk.ImageFileReader[ImageType].New()

diretoriasDataSets = []
dataSets = []

# Carregam-se as diretorias de todos os datasets.
for diretoriaDataSet in listdir(diretoriaDataSets):
    diretoriasDataSets.append(os.path.join(diretoriaDataSets, diretoriaDataSet))
print(diretoriasDataSets)

# Carregam-se todos os datasets.
for diretoriaDataSet in diretoriasDataSets:
    reader.SetFileName(diretoriaDataSet)
    reader.Update()
    dataSets.append(reader.GetOutput())
print(dataSets)