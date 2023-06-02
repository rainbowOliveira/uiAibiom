"""
Module: SceneViewerAPP.py
@author: Carlos Vinhais
cvinhais@gmail.com
"""

import sys
import numpy as np

from PyQt5 import Qt, QtWidgets # QtCore, QtGui,
from PyQt5.QtWidgets import QApplication, QMessageBox

import SceneViewerGUI

""" A class for Scene Viewer APP """

class SceneViewerApp( QtWidgets.QMainWindow ):
 
    def __init__(self, parent=None):

        # Parent constructor
        super( SceneViewerApp, self).__init__()
        self.ui = SceneViewerGUI.Ui_MainWindow()
        self.ui.setupUi(self)

        # ========================================================
        self.APP_NAME    = "SceneViewerApp"
        self.APP_VERSION = "v0"
        # ========================================================

        # APP Callbacks - "Menu -> File, Help"
        self.ui.FileQuitAction.triggered.connect(  self.File_Quit )
        self.ui.HelpAboutAction.triggered.connect( self.Help_About )
        
        # APP Button Callbacks
        self.ui.button_Apply.clicked.connect( self.Apply )
        self.ui.button_Reset.clicked.connect( self.Reset )
        self.ui.button_Start.clicked.connect( self.Start )
        self.ui.button_Stop.clicked.connect(  self.Stop )
     
        self.flag_STOP = 0


    # ===========================================================
    # # APP Button Callbacks
    # ===========================================================

    def Apply(self):
        self.ui.SetMessageStatus( 'Apply Button clicked!' )
        # -----------------------------------
        label  = str(   self.ui.lineEdit.text() )
        Ns     = int(   self.ui.spinBox1.value() )
        factor = float( self.ui.spinBox2.value() )
        flag1  = bool ( self.ui.checkBox.isChecked() )
        if   ( self.ui.radio1.isChecked() ): flag2 = 0;
        elif ( self.ui.radio2.isChecked() ): flag2 = 1;
        # -----------------------------------
        print ("label  =", label)
        print ("Ns     =", Ns)
        print ("factor =", factor)
        print ("flag1  =", flag1)
        print ("flag2  =", flag2)
        print ("")
        # -----------------------------------
        self.ui.SetMessageStatus('Ready.')


    def Reset(self):
        self.ui.SetMessageStatus( 'Reset Button clicked!' )
        # -----------------------------------
        self.ui.lineEdit.setText( "reseted" )
        self.ui.spinBox1.setValue( 100 )
        self.ui.spinBox2.setValue( 0.5 )
        self.ui.checkBox.setChecked( False )
        # -----------------------------------
        self.ui.progressBar.setValue( 0 )
        # -----------------------------------
        # self.ui.table1.setRowCount( 1 )
        # self.ui.table1.setItem(0, 0, QtWidgets.QTableWidgetItem(""))
        # self.ui.table1.setItem(0, 1, QtWidgets.QTableWidgetItem(""))
        # self.ui.table1.setItem(0, 2, QtWidgets.QTableWidgetItem(""))        
        # -----------------------------------
        self.ui.qvtk1.CleanViewer()
        # -----------------------------------
        self.ui.SetMessageStatus('Ready.') 
        

    def Start(self):
        self.ui.SetMessageStatus( 'Start Button clicked!' )
        self.ui.button_Start.setEnabled( 0 )
        self.ui.button_Stop.setEnabled( 1 ) 
        # -----------------------------------
        Ns = self.ui.spinBox1.value()

        # Simulation Demo -
        # ----------------------
        for n in range(0, Ns ):

            # do something ...

            progress = 100.0 * (n + 1)/Ns
            self.ui.progressBar.setValue( progress )

            if ( self.flag_STOP ):
                self.flag_STOP = 0
                break
        # -----------------------------------
        self.ui.button_Start.setEnabled( 1 )
        self.ui.button_Stop.setEnabled( 0 ) 
        self.ui.SetMessageStatus('Ready.') 


    def Stop(self):
        self.ui.SetMessageStatus( 'Stop Button clicked!' )
        # -----------------------------------
        self.flag_STOP = 1     
        # -----------------------------------        
        self.ui.button_Start.setEnabled( 1 )
        self.ui.button_Stop.setEnabled( 0 )
        self.ui.SetMessageStatus('Ready.')


    # ===========================================================
    # APP Menu Bar Callbacks
    # ===========================================================

    def Help_About(self): # QMessageBox.information
        self.ui.statusBar.showMessage('About...')
        # -----------------------------------------
        message = self.APP_NAME + " - " + str( self.APP_VERSION ) + "\n"
        message += "\n"
        message += "\n"
        message += "CAV @ 2020" + "\n"
        QtWidgets.QMessageBox.information(QtWidgets.QWidget(), 'About', message)
        # ----------------------------------------- 
        self.ui.statusBar.showMessage('Ready.')


    def File_Quit(self):  # QMessageBox.question
        self.ui.statusBar.showMessage('Quit...')
        # -----------------------------------------    
        buttonReply = QMessageBox.question(self, 'APP message', "Do you want to Quit?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.hide()
            QApplication.quit()
            # sys.exit()
        else:
            pass
        # ----------------------------------------- 
        self.ui.statusBar.showMessage('Ready.')


# ===============================================
if __name__ == "__main__": 
    app = Qt.QApplication(sys.argv)
    myapp = SceneViewerApp()
    myapp.show()
    sys.exit(app.exec_())
    # app.quit()
# ===============================================