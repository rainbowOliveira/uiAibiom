"""
Module: SceneViewerGUI.py
@author: Carlos Vinhais
cvinhais@gmail.com
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import ( QApplication, QStyle, QMenu, QAction,
QVBoxLayout, QHBoxLayout, QGridLayout, QFrame,
QLineEdit, QComboBox, QCheckBox, QProgressBar,
QRadioButton, QPushButton, QGroupBox, QLabel,
QSpinBox, QDoubleSpinBox )

import SceneViewer

""" A class for Scene Viewer GUI """

class Ui_MainWindow( object ):
    
    def setupUi(self, MainWindow):
        
        QApplication.setStyle('Fusion')
         
        # Main Window
        # -------------------------------------
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Scene Viewer App")
        MainWindow.setWindowIcon( QtGui.QIcon('pythonlogo.png') )

        self.centralWidget = QtWidgets.QWidget( MainWindow )
        # MainWindow.setCentralWidget( self.centralWidget )
        
        # Widgets
        # -------------------------------------
        self.SettingsGroup("Settings")
        self.ParametersGroup("Parameters")
        self.EngineGroup("Engine")
        self.ProgressGroup("Progess")
        
        self.qvtk1 = SceneViewer.SceneViewer( MainWindow )
        self.qvtk2 = SceneViewer.SceneViewer( MainWindow )

        # Layouts
        # -------------------------------------
        layout1 = QVBoxLayout()
        layout1.setContentsMargins(0,0,0,0)
        layout1.addWidget( self.SettingsGroup )
        layout1.addWidget( self.ParametersGroup )
        layout1.addWidget( self.EngineGroup )
        layout1.addWidget( self.ProgressGroup )
        layout1.setAlignment( QtCore.Qt.AlignTop )       

        layout2 = QHBoxLayout()
        layout2.setContentsMargins(0,0,0,0)
        layout2.addWidget( self.qvtk1.iren )
        # layout2.addWidget( self.qvtk2.iren )
        
        layout = QHBoxLayout()
        layout.addLayout( layout1 )
        layout.addLayout( layout2 )
        
        # Frame
        # ------------------------------------- 
        self.frame = QFrame( self.centralWidget )
        self.frame.setFrameShape( QFrame.StyledPanel )
        self.frame.setLayout( layout )
        
        MainWindow.setCentralWidget( self.frame )

        # Menu Bar
        # -------------------------------------
        self.FileMenu = QMenu("&File")
        self.HelpMenu = QMenu("&Help")
        
        self.menuBar = MainWindow.menuBar()
        self.menuBar.addMenu( self.FileMenu )
        self.menuBar.addMenu( self.HelpMenu )
        
        self.FileNewAction    = self.FileMenu.addAction('N&ew...')
        self.FileOpenAction   = self.FileMenu.addAction('O&pen...')
        self.FileExportAction = self.FileMenu.addAction('Ex&port...')
        self.FileQuitAction   = self.FileMenu.addAction('Quit')
        self.FileNewAction.setShortcut('Ctrl+N')
        self.FileOpenAction.setShortcut('Ctrl+O')
        self.FileExportAction.setShortcut('Ctrl+X')
        self.FileQuitAction.setShortcut('Ctrl+Q')
        
        self.HelpAboutAction = self.HelpMenu.addAction('About')
        self.HelpAboutAction.setShortcut('Ctrl+A')
        
        # Tool Bar
        # -------------------------------------
        icons = [
            'SP_DialogOpenButton',
            'SP_DialogApplyButton',
            'SP_DialogCancelButton',
            'SP_DialogResetButton',
            'SP_DialogDiscardButton',            
            'SP_DialogSaveButton',
            'SP_DialogCloseButton',
            'SP_DialogHelpButton',            
            'SP_CustomBase',
            'SP_ArrowBack',
            'SP_ArrowDown']
        # self.toolbar = MainWindow.addToolBar( '' )
        # for i in icons:        
        #     img = MainWindow.style().standardIcon(getattr(QStyle, i))
        #     action = QAction( img, i, MainWindow)
        #     action.setEnabled( 1 )
        #     self.toolbar.addAction( action ) 

        self.toolbar = MainWindow.addToolBar( '' )
        icon = 'SP_DialogOpenButton'
        img = MainWindow.style().standardIcon(getattr(QStyle, icon))
        self.action = QAction( img, icon, MainWindow)
        self.toolbar.addAction( self.action )
        # self.action.triggered.connect( ... )
        
        # Status Bar
        # -------------------------------------
        self.statusBar = MainWindow.statusBar()
        self.statusBar.showMessage('Ready.')

    def SetMessageStatus(self, message ):
        self.statusBar.showMessage( message )

    # ===============================================

    def SettingsGroup(self, title):
        # Widgets
        lineEditLabel = QLabel("Label")
        self.lineEdit = QLineEdit( "my label" ) # default value
        # Layout
        layout = QGridLayout()
        layout.addWidget( lineEditLabel, 0, 0)
        layout.addWidget( self.lineEdit, 1, 0)
        # Group
        self.SettingsGroup = QGroupBox( title )
        self.SettingsGroup.setStyleSheet("QGroupBox { font-weight: bold; } ")        
        self.SettingsGroup.setLayout( layout )        

    # -------------------------------------

    def ParametersGroup(self, title):
        # Widgets
        spinBoxLabel1 = QLabel("Samples, Ns")
        self.spinBox1 = QSpinBox()
        self.spinBox1.setSingleStep( 1 )
        self.spinBox1.setRange(1, 500)
        self.spinBox1.setValue( 100 )  
        self.spinBox1.setEnabled( 1 )
       
        spinBoxLabel2 = QLabel("Factor, f")
        self.spinBox2 = QDoubleSpinBox()
        self.spinBox2.setDecimals( 2 )
        self.spinBox2.setSingleStep( 0.01 )
        self.spinBox2.setRange(0, 1)
        self.spinBox2.setValue( 100.00 )  
        self.spinBox2.setEnabled( 1 )
        
        comboBoxLabel = QLabel("Distribution")
        self.comboBox = QComboBox()
        self.comboBox.addItem("uniform")
        self.comboBox.addItem("normal")
        self.comboBox.setEnabled( 1 )

        checkBoxLabel = QLabel("Ckeck")
        self.checkBox = QCheckBox("ckeck")
        self.checkBox.setChecked( False )
        self.checkBox.setEnabled( 1 )

        self.radio1 = QRadioButton("radio1")
        self.radio2 = QRadioButton("radio2")
        self.radio1.setChecked( True )
        self.radio2.setChecked( False )  

        self.toggleButton = QPushButton( "&Toggle Button" )
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked( True )
        
        # Layout
        layout = QGridLayout()
        layout.addWidget(spinBoxLabel1, 0, 0)
        layout.addWidget(self.spinBox1, 0, 1)
        layout.addWidget(spinBoxLabel2, 1, 0)
        layout.addWidget(self.spinBox2, 1, 1)
        layout.addWidget(comboBoxLabel, 2, 0)
        layout.addWidget(self.comboBox, 2, 1)
        layout.addWidget(checkBoxLabel, 3, 0)
        layout.addWidget(self.checkBox, 3, 1)
        layout.addWidget( self.radio1,  4, 0)
        layout.addWidget( self.radio2,  4, 1)
        layout.addWidget( self.toggleButton, 5, 0, 1, 2)
       
        # Group
        self.ParametersGroup = QGroupBox( title )
        self.ParametersGroup.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ParametersGroup.setLayout( layout )

        # Callbacks
        self.toggleButton.clicked.connect( self.toggleCallback )

    # -------------------------------------
    
    def EngineGroup(self, title):

        # Widgets: Buttons: UI Actions
        self.button_Apply = QPushButton( "Apply" )
        self.button_Reset = QPushButton( "Reset" )
        self.button_Start = QPushButton( "Start" )
        self.button_Stop  = QPushButton( "Stop"  )
        
        icon1 = 'SP_DialogApplyButton'
        icon2 = 'SP_DialogResetButton'
        icon3 = 'SP_DialogCancelButton'
        img1 = self.centralWidget.style().standardIcon(getattr(QStyle, icon1))
        img2 = self.centralWidget.style().standardIcon(getattr(QStyle, icon2))
        img3 = self.centralWidget.style().standardIcon(getattr(QStyle, icon3))

        self.button_Apply.setIcon( img1 )
        self.button_Reset.setIcon( img2 )
        self.button_Start.setIcon( img1 )
        self.button_Stop.setIcon(  img3 )

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.button_Apply,  0, 0)
        layout.addWidget(self.button_Reset,  0, 1)
        layout.addWidget(self.button_Start,  1, 0)
        layout.addWidget(self.button_Stop,   1, 1)
               
        # Group
        self.EngineGroup = QGroupBox( title )
        self.EngineGroup.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.EngineGroup.setLayout( layout )

    # ----------------------------------------------------------

    def ProgressGroup(self, title):
        # Widgets
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible( 1 )
        self.progressBar.setRange( 0, 100 )
        self.progressBar.setValue( 0 )
        #self.ui.progressBar.setMinimum( 0 )
        #self.ui.progressBar.setMaximum( 100 )
        # Layout
        layout = QGridLayout()
        layout.addWidget( self.progressBar, 0, 0)
        # Group
        self.ProgressGroup = QGroupBox( title )
        self.ProgressGroup.setStyleSheet("QGroupBox { font-weight: bold; } ") 
        self.ProgressGroup.setLayout( layout )


    # ===========================================================
    # Q Callbacks
    # ===========================================================

    def toggleCallback(self):
        print ("toggle Button clicked!")
        if ( self.toggleButton.isChecked() ):
            print("isChecked" )
        else:
            print ("not Checked")

    def myFakeCallBack(self):        
        print ('Hello World')
        
# ===========================================================	
# EOF.
