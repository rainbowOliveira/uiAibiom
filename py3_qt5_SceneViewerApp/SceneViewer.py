"""
Module: SceneViewer.py
@author: Carlos Vinhais
cvinhais@gmail.com
"""

import sys
import vtk
import random

from PyQt5 import QtGui, QtWidgets # QtCore,
from PyQt5.QtWidgets import QApplication
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

#  cvCOLORMAP_JET
RED   = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.00588235294117645,0.02156862745098032,0.03725490196078418,0.05294117647058827,0.06862745098039214,0.084313725490196,0.1000000000000001,0.115686274509804,0.1313725490196078,0.1470588235294117,0.1627450980392156,0.1784313725490196,0.1941176470588235,0.2098039215686274,0.2254901960784315,0.2411764705882353,0.2568627450980392,0.2725490196078431,0.2882352941176469,0.303921568627451,0.3196078431372549,0.3352941176470587,0.3509803921568628,0.3666666666666667,0.3823529411764706,0.3980392156862744,0.4137254901960783,0.4294117647058824,0.4450980392156862,0.4607843137254901,0.4764705882352942,0.4921568627450981,0.5078431372549019,0.5235294117647058,0.5392156862745097,0.5549019607843135,0.5705882352941174,0.5862745098039217,0.6019607843137256,0.6176470588235294,0.6333333333333333,0.6490196078431372,0.664705882352941,0.6803921568627449,0.6960784313725492,0.7117647058823531,0.7274509803921569,0.7431372549019608,0.7588235294117647,0.7745098039215685,0.7901960784313724,0.8058823529411763,0.8215686274509801,0.8372549019607844,0.8529411764705883,0.8686274509803922,0.884313725490196,0.8999999999999999,0.9156862745098038,0.9313725490196076,0.947058823529412,0.9627450980392158,0.9784313725490197,0.9941176470588236,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.9862745098039216,0.9705882352941178,0.9549019607843139,0.93921568627451,0.9235294117647062,0.9078431372549018,0.892156862745098,0.8764705882352941,0.8607843137254902,0.8450980392156864,0.8294117647058825,0.8137254901960786,0.7980392156862743,0.7823529411764705,0.7666666666666666,0.7509803921568627,0.7352941176470589,0.719607843137255,0.7039215686274511,0.6882352941176473,0.6725490196078434,0.6568627450980391,0.6411764705882352,0.6254901960784314,0.6098039215686275,0.5941176470588236,0.5784313725490198,0.5627450980392159,0.5470588235294116,0.5313725490196077,0.5156862745098039,0.5)
GREEN = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.001960784313725483,0.01764705882352935,0.03333333333333333,0.0490196078431373,0.06470588235294117,0.08039215686274503,0.09607843137254901,0.111764705882353,0.1274509803921569,0.1431372549019607,0.1588235294117647,0.1745098039215687,0.1901960784313725,0.2058823529411764,0.2215686274509804,0.2372549019607844,0.2529411764705882,0.2686274509803921,0.2843137254901961,0.3,0.3156862745098039,0.3313725490196078,0.3470588235294118,0.3627450980392157,0.3784313725490196,0.3941176470588235,0.4098039215686274,0.4254901960784314,0.4411764705882353,0.4568627450980391,0.4725490196078431,0.4882352941176471,0.503921568627451,0.5196078431372548,0.5352941176470587,0.5509803921568628,0.5666666666666667,0.5823529411764705,0.5980392156862746,0.6137254901960785,0.6294117647058823,0.6450980392156862,0.6607843137254901,0.6764705882352942,0.692156862745098,0.7078431372549019,0.723529411764706,0.7392156862745098,0.7549019607843137,0.7705882352941176,0.7862745098039214,0.8019607843137255,0.8176470588235294,0.8333333333333333,0.8490196078431373,0.8647058823529412,0.8803921568627451,0.8960784313725489,0.9117647058823528,0.9274509803921569,0.9431372549019608,0.9588235294117646,0.9745098039215687,0.9901960784313726,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.9901960784313726,0.9745098039215687,0.9588235294117649,0.943137254901961,0.9274509803921571,0.9117647058823528,0.8960784313725489,0.8803921568627451,0.8647058823529412,0.8490196078431373,0.8333333333333335,0.8176470588235296,0.8019607843137253,0.7862745098039214,0.7705882352941176,0.7549019607843137,0.7392156862745098,0.723529411764706,0.7078431372549021,0.6921568627450982,0.6764705882352944,0.6607843137254901,0.6450980392156862,0.6294117647058823,0.6137254901960785,0.5980392156862746,0.5823529411764707,0.5666666666666669,0.5509803921568626,0.5352941176470587,0.5196078431372548,0.503921568627451,0.4882352941176471,0.4725490196078432,0.4568627450980394,0.4411764705882355,0.4254901960784316,0.4098039215686273,0.3941176470588235,0.3784313725490196,0.3627450980392157,0.3470588235294119,0.331372549019608,0.3156862745098041,0.2999999999999998,0.284313725490196,0.2686274509803921,0.2529411764705882,0.2372549019607844,0.2215686274509805,0.2058823529411766,0.1901960784313728,0.1745098039215689,0.1588235294117646,0.1431372549019607,0.1274509803921569,0.111764705882353,0.09607843137254912,0.08039215686274526,0.06470588235294139,0.04901960784313708,0.03333333333333321,0.01764705882352935,0.001960784313725483,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
BLUE  = (0.5,0.5156862745098039,0.5313725490196078,0.5470588235294118,0.5627450980392157,0.5784313725490196,0.5941176470588235,0.6098039215686275,0.6254901960784314,0.6411764705882352,0.6568627450980392,0.6725490196078432,0.6882352941176471,0.7039215686274509,0.7196078431372549,0.7352941176470589,0.7509803921568627,0.7666666666666666,0.7823529411764706,0.7980392156862746,0.8137254901960784,0.8294117647058823,0.8450980392156863,0.8607843137254902,0.8764705882352941,0.892156862745098,0.907843137254902,0.9235294117647059,0.9392156862745098,0.9549019607843137,0.9705882352941176,0.9862745098039216,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.9941176470588236,0.9784313725490197,0.9627450980392158,0.9470588235294117,0.9313725490196079,0.915686274509804,0.8999999999999999,0.884313725490196,0.8686274509803922,0.8529411764705883,0.8372549019607844,0.8215686274509804,0.8058823529411765,0.7901960784313726,0.7745098039215685,0.7588235294117647,0.7431372549019608,0.7274509803921569,0.7117647058823531,0.696078431372549,0.6803921568627451,0.6647058823529413,0.6490196078431372,0.6333333333333333,0.6176470588235294,0.6019607843137256,0.5862745098039217,0.5705882352941176,0.5549019607843138,0.5392156862745099,0.5235294117647058,0.5078431372549019,0.4921568627450981,0.4764705882352942,0.4607843137254903,0.4450980392156865,0.4294117647058826,0.4137254901960783,0.3980392156862744,0.3823529411764706,0.3666666666666667,0.3509803921568628,0.335294117647059,0.3196078431372551,0.3039215686274508,0.2882352941176469,0.2725490196078431,0.2568627450980392,0.2411764705882353,0.2254901960784315,0.2098039215686276,0.1941176470588237,0.1784313725490199,0.1627450980392156,0.1470588235294117,0.1313725490196078,0.115686274509804,0.1000000000000001,0.08431372549019622,0.06862745098039236,0.05294117647058805,0.03725490196078418,0.02156862745098032,0.00588235294117645,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
def randomColor():    
    c = random.randint(0,255)
    color = RED[c], GREEN[c], BLUE[c]
    return color


""" A class for VTK Scene Viewer """

class SceneViewer( QtWidgets.QWidget ):
    
    def __init__(self, parent=None):

        # Widget
        QtWidgets.QWidget.__init__(self, parent)
        # QtGui.QFrame.__init__(self, parent) 
        # QtGui.QGroupBox.__init__(self, parent) 

        # Main Window
        # -------------------------------------
        self.setObjectName("SceneViewer")
        self.setWindowTitle("Scene Viewer")
        self.setWindowIcon( QtGui.QIcon('icon.png') )
        # self.resize(512,512)
        
        # Setup VTK environment
        self.iren = QVTKRenderWindowInteractor(self) # can be re parented
        # self.iren.setFixedWidth( fixedWidth )
        # self.iren.setFixedHeight( fixedHeight )
        
        self.CreateVTKRenderer()
        self.CreateAxes()
        self.CreateUnitSphere()
        self.CreateXYPlane()
        self.Initialize()
        
        # Q Controls
        self._CreateVTKViewerGroup( "Scene Viewer" ) 
        self._CreateVTKModelGroup( "Model Data" )
        self._CreateVTKButtonGroup( "Actions" )

        # Q Layout
        layout = QtWidgets.QGridLayout()        
        layout.addWidget( self.iren,           0, 0, 1, 3 )
        layout.addWidget( self.vtkViewerGroup, 1, 0, 1, 1 )
        layout.addWidget( self.vtkModelGroup,  1, 1, 1, 1 )
        layout.addWidget( self.vtkButtonGroup, 1, 2, 1, 1 )        
        self.setLayout( layout )


    def CreateVTKRenderer(self):        
        # renderer
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0.25, 0.25, 0.25)
#        self.ren.SetBackground(0.2, 0.2, 0.2)
#        self.ren.SetBackground(1.0,1.0,1.0)
#        self.ren.SetBackground(0.0,0.0,0.0)
        
        # renderer window
        self.renWin = self.iren.GetRenderWindow()
        self.renWin.AddRenderer( self.ren )
        #self.iren.SetInteractorStyle( vtk.vtkInteractorStyleTrackballCamera() )
        self.renWin.SetInteractor( self.iren )

        self.cornerAnnotation = vtk.vtkCornerAnnotation()
        self.cornerAnnotation.SetLinearFontScaleFactor(2)
        self.cornerAnnotation.SetNonlinearFontScaleFactor(1)
        self.cornerAnnotation.SetMaximumFontSize(15)
        self.cornerAnnotation.GetTextProperty().SetColor(1, 1, 1)
        self.cornerAnnotation.SetText(0, "corner 0" ) # m_TextAnnotation0.c_str() )
        self.cornerAnnotation.SetText(1, "corner 1" ) # m_TextAnnotation1.c_str() )
        self.cornerAnnotation.SetText(2, "corner 2" ) # m_TextAnnotation2.c_str() )
        self.cornerAnnotation.SetText(3, "corner 3" ) # m_TextAnnotation3.c_str() )
        
        self.ren.AddViewProp( self.cornerAnnotation )  
       
    def CreateAxes(self):
        # axesActor
        self.axesActor = vtk.vtkAxesActor()
        self.ren.AddActor( self.axesActor )

        # OrientationMarker 
        self.markerActor = vtk.vtkAxesActor()
        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker( self.markerActor )
        self.axes.SetInteractor( self.iren )
        self.axes.EnabledOn()
        self.axes.InteractiveOn()

    def CreateUnitSphere(self):
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetRadius( 1 )
        sphereSource.SetThetaResolution( 36 )
        sphereSource.SetPhiResolution( 18 )
        sphereSource.Update()  
        
        self.unitSphere = vtk.vtkPolyData()
        self.unitSphere = sphereSource.GetOutput()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData( self.unitSphere )
        self.unitSphereActor = vtk.vtkActor()
        self.unitSphereActor.SetMapper( mapper )        
        self.unitSphereActor.GetProperty().SetColor( 1, 0, 0 ) # (R,G,B)
        self.unitSphereActor.GetProperty().SetOpacity( 0.5 )
        self.ren.AddActor( self.unitSphereActor )
    #    actor.GetProperty().EdgeVisibilityOn() 
    #    actor.GetProperty().SetEdgeColor( 0.75, 0.75, 0.75)
    #    actor.SetTexture( texture )

    def CreateXYPlane(self):
        planeSource = vtk.vtkPlaneSource()
        planeSource.SetXResolution( 10 )
        planeSource.SetYResolution( 10 )    
        planeSource.SetOrigin( -5, -5, 0 )
        planeSource.SetPoint1(  5, -5, 0 )
        planeSource.SetPoint2( -5,  5, 0 )
        planeSource.Update()    
        plane = vtk.vtkPolyData()
        plane = planeSource.GetOutput()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData( plane )
        self.planeActor = vtk.vtkActor()
        self.planeActor.SetMapper( mapper )
        self.planeActor.GetProperty().EdgeVisibilityOn() 
        self.planeActor.GetProperty().SetEdgeColor( 1, 1, 1)
        self.planeActor.GetProperty().SetOpacity( 0.5 )
        self.ren.AddActor( self.planeActor )

    def DisplaySphere(self, center, radius):
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter( center )
        sphereSource.SetRadius( radius )
        sphereSource.SetThetaResolution( 36 )
        sphereSource.SetPhiResolution( 18 )
        sphere = vtk.vtkPolyData()
        sphere = sphereSource.GetOutput()
        sphere.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData( sphere )
        actor = vtk.vtkActor()
        actor.GetProperty().SetColor( 1,1,1 ) # (R,G,B)
        #actor.GetProperty().EdgeVisibilityOn() 
        #actor.GetProperty().SetEdgeColor( 0.75, 0.75, 0.75)
        actor.GetProperty().SetOpacity( 0.5 )
        #actor.SetTexture( texture )
        actor.SetMapper( mapper )
        self.ren.AddActor( actor )
    
    def Initialize(self):
        self.ren.ResetCamera()
        self.renWin.Render()
        self.iren.Initialize()
        self.iren.Start()   

    # ===========================================================
    # OBJECTS
    # ===========================================================    
        
    def DisplayPolyData(self, polydata, opacity, withedges ):
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData( polydata )
        actor = vtk.vtkActor()
        #actor.GetProperty().SetColor( randomColor() ) # ( 0.5, 0.5, 0.5 )
        #actor.GetProperty().SetColor( 0.75, 0.75, 0.75 )
        actor.GetProperty().SetOpacity( opacity )
        #actor.GetProperty().BackfaceCullingOn()
        actor.SetMapper( mapper )
        if ( withedges == 1 ):
#            actor.GetProperty().SetEdgeColor(1.0, 1.0, 1.0)
            actor.GetProperty().SetEdgeColor(1.0, 0.0, 0.0) # RED
#            actor.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)
            actor.GetProperty().EdgeVisibilityOn()    
        self.ren.AddActor( actor )

    def GlyphPoints(self, shape, radius ):
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius( radius )
        glyph = vtk.vtkGlyph3D()
        glyph.SetInputData( shape )
        glyph.SetSourceConnection( sphere.GetOutputPort() )
        glyph.GeneratePointIdsOn()
        glyph.Update()   
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData( glyph.GetOutput() )
        actor = vtk.vtkActor()
        actor.GetProperty().SetColor( randomColor() ) # (R,G,B)
        actor.SetMapper( mapper )
        self.ren.AddActor( actor )

    def LabelPoints(self, shape ):
        mapper = vtk.vtkLabeledDataMapper()
        mapper.SetInputData( shape )

#        mapper.SetLabelModeToLabelIds()
        # or
        mapper.SetFieldDataName( "labels" )
        mapper.SetLabelModeToLabelFieldData()
        #mapper.SetFieldDataArray( 2 )

        actor = vtk.vtkActor2D()
        actor.GetProperty().SetColor( randomColor() ) # (R,G,B)
        actor.SetMapper( mapper )
        self.ren.AddActor( actor )


    def DisplayCenterline(self, centerline, radius, scale, flag ):
        self.GlyphPoints( centerline, radius )
        self.GlyphFrenet( centerline, scale )
        if ( flag ):
            self.LabelPoints( centerline )
        
    def GlyphFrenet(self, centerline, scale ):
        centerline.GetPointData().SetActiveVectors( "FSNormals")
        self.GlyphVectors( centerline, scale, [1,0,0] ) # X = RED
        centerline.GetPointData().SetActiveVectors( "FSBinormals" )
        self.GlyphVectors( centerline, scale, [0,1,0] ) # Y = GREEN
        centerline.GetPointData().SetActiveVectors( "FSTangents" )
        self.GlyphVectors( centerline, scale, [0,0,1] ) # Z = BLUE 
    
    def GlyphVectors(self, polydata, scale, color ):
        arrow = vtk.vtkArrowSource()
        glyph = vtk.vtkGlyph3D()
        glyph.SetSourceConnection( arrow.GetOutputPort() )
        glyph.SetInput( polydata ) 
        glyph.SetVectorModeToUseVector()
        glyph.SetScaleModeToScaleByVector()
        glyph.SetScaleFactor( scale ) # 
        glyph.OrientOn()
        glyph.Update()
        gPolyData = vtk.vtkPolyData()
        gPolyData.DeepCopy( glyph.GetOutput() )
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData( gPolyData )
        mapper.SetScalarModeToUsePointFieldData()
        actor = vtk.vtkActor()
        actor.SetMapper( mapper )
        actor.GetProperty().SetColor( color ) # (R,G,B)
        self.ren.AddActor( actor )
            
    def GlyphNormals(self, polydata, scale ):
        # Source for the glyph filter
        arrow = vtk.vtkArrowSource()
        arrow.Update() 
        #arrow.SetTipResolution( 16 )
        #arrow.SetTipLength( 0.3 )
        #arrow.SetTipRadius( 0.1 )
        ## Choose a random subset of polydata points.
        #maskPts = vtk.vtkMaskPoints()
        #maskPts.SetOnRatio( 5 )
        #maskPts.SetInput( polydata )
        #maskPts.Update()    
        #glyph.SetInput( maskPts.GetOutput() )
        glyph = vtk.vtkGlyph3D()
        glyph.SetSourceConnection( arrow.GetOutputPort() )
        glyph.SetInput( polydata )
        #glyph.SetInput( maskPts.GetOutput() )
        glyph.SetVectorModeToUseNormal()
        glyph.SetScaleModeToScaleByVector()
        glyph.SetScaleFactor( scale )
        glyph.SetColorModeToColorByVector()
        glyph.OrientOn()
        glyph.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection( glyph.GetOutputPort() )
        mapper.SetScalarModeToUsePointFieldData()
    #    mapper.SetColorModeToMapScalars()
    #    mapper.ScalarVisibilityOn()
        actor = vtk.vtkActor()
        actor.SetMapper( mapper )
        actor.GetProperty().SetColor( [1,0,0] ) # (R,G,B)
        self.ren.AddActor( actor )    

    def DisplayLineBetweenTwoPoints( self, p1, p2 ):
        points = vtk.vtkPoints()
        points.InsertNextPoint( p1 )
        points.InsertNextPoint( p2 )
        line = vtk.vtkLine()               # Create the first line (between Origin and P0)
        line.GetPointIds().SetId(0, 0)     # the second 0 is the index of the Origin in the vtkPoints
        line.GetPointIds().SetId(1, 1)     # the second 1 is the index of P0 in the vtkPoints
        lines = vtk.vtkCellArray()         # Create the topology of the point (a vertex)
        lines.InsertNextCell( line )

        path = vtk.vtkPolyData()
        path.SetPoints( points )
        path.SetLines( lines )

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData( path )
        
        actor = vtk.vtkActor()
        actor.GetProperty().SetEdgeColor( 1.0, 1.0, 1.0 )
        actor.GetProperty().EdgeVisibilityOn()   
        actor.SetMapper( mapper )
        self.ren.AddActor( actor )
        

    # ===========================================================
    # Q Control Groups
    # ===========================================================  
        
    def _CreateVTKViewerGroup(self, title ):
        self.vtkViewerGroup = QtWidgets.QGroupBox( title )
        self.vtkViewerGroup.setStyleSheet("QGroupBox { font-weight: bold; } ")
        
        # Check Box
        self.checkBox0 = QtWidgets.QCheckBox("World Axes")
        self.checkBox1 = QtWidgets.QCheckBox("Unit Sphere")
        self.checkBox2 = QtWidgets.QCheckBox("WXY Plane") 
        self.checkBox0.setChecked( True )
        self.checkBox1.setChecked( True )
        self.checkBox2.setChecked( True )        

        # Layout
        layout = QtWidgets.QGridLayout()        
        layout.addWidget( self.checkBox0, 0, 0 )
        layout.addWidget( self.checkBox1, 1, 0 )
        layout.addWidget( self.checkBox2, 2, 0 )
        self.vtkViewerGroup.setLayout( layout )
        
        # Callbacks
        self.checkBox0.clicked.connect( self.SetSceneVisibility )
        self.checkBox1.clicked.connect( self.SetSceneVisibility )
        self.checkBox2.clicked.connect( self.SetSceneVisibility )


    def _CreateVTKModelGroup(self, title ):
        self.vtkModelGroup = QtWidgets.QGroupBox( title )
        self.vtkModelGroup.setStyleSheet("QGroupBox { font-weight: bold; } ")

        # Check Box: mesh
        self.checkBox3 = QtWidgets.QCheckBox("centerline")        
        self.checkBox4 = QtWidgets.QCheckBox("mesh")
        self.checkBox5 = QtWidgets.QCheckBox("rings")
        self.checkBox3.setChecked( True )
        self.checkBox4.setChecked( True )
        self.checkBox5.setChecked( True ) 
        
        # check boxes: cell data
#        self.checkBox6 = QtWidgets.QCheckBox("area")        
#        self.checkBox7 = QtWidgets.QCheckBox("frame")
#        self.checkBox8 = QtWidgets.QCheckBox("radii")
        
        # Layout
        layout = QtWidgets.QGridLayout()        
        layout.addWidget( self.checkBox3, 0, 0 )
        layout.addWidget( self.checkBox4, 1, 0 )
        layout.addWidget( self.checkBox5, 2, 0 )
#        layout.addWidget( self.checkBox6, 0, 1 )
#        layout.addWidget( self.checkBox7, 1, 1 )
#        layout.addWidget( self.checkBox8, 2, 1 )
        self.vtkModelGroup.setLayout( layout )
        

    def _CreateVTKButtonGroup(self, title ):
        self.vtkButtonGroup = QtWidgets.QGroupBox( title )
        self.vtkButtonGroup.setStyleSheet("QGroupBox { font-weight: bold; } ")
        
        # UI Buttons
        self.button_Reset = QtWidgets.QPushButton( "Reset Camera" )
        self.button_Clean = QtWidgets.QPushButton( "Clear Viewer" )
        self.button_Write = QtWidgets.QPushButton( "Write to PNG" )
        icon1 = 'SP_DialogHelpButton'
        icon2 = 'SP_DialogResetButton'
        icon3 = 'SP_DialogSaveButton'
        img1 = self.style().standardIcon(getattr(QtWidgets.QStyle, icon1))
        img2 = self.style().standardIcon(getattr(QtWidgets.QStyle, icon2))
        img3 = self.style().standardIcon(getattr(QtWidgets.QStyle, icon3))
        self.button_Reset.setIcon( img1 )
        self.button_Clean.setIcon( img2 )
        self.button_Write.setIcon( img3 )
        
        # Layout
        layout = QtWidgets.QGridLayout()        
        layout.addWidget( self.button_Reset, 0, 0 )
        layout.addWidget( self.button_Clean, 1, 0 )
        layout.addWidget( self.button_Write, 2, 0 )
        self.vtkButtonGroup.setLayout( layout )
        
        # Callbacks
        self.button_Reset.clicked.connect( self.ResetCamera )
#        self.button_Clean.clicked.connect( self.CleanViewer )
        self.button_Write.clicked.connect( self.WriteScreenShot )
    
    # ===========================================================
    # Q Callbacks
    # ===========================================================

    def SetSceneVisibility(self):
        self.axesActor.SetVisibility( self.checkBox0.isChecked() )
        self.unitSphereActor.SetVisibility( self.checkBox1.isChecked() )
        self.planeActor.SetVisibility( self.checkBox2.isChecked() )
        self.renWin.Render()

    def ResetCamera(self):        
        self.ren.ResetCamera()
        self.renWin.Render()

    def SetCamera(self, position, focus ):
        camera = vtk.vtkCamera()
        camera.SetPosition( position )
        camera.SetFocalPoint( focus )
        self.ren.SetActiveCamera( camera )
        self.renWin.Render()
##        m_shape -> GetPoint( static_cast<vtkIdType>( m_selectedID ), L);
#        self.ren.GetActiveCamera().SetFocalPoint( focus )
#        self.ren.GetActiveCamera().SetPosition( position )
#        self.renWin.Render()   

    def CleanViewer(self):
        self.ren.RemoveAllViewProps()
        self.ren.AddActor( self.axesActor )
        self.ren.AddActor( self.unitSphereActor )
        self.ren.AddActor( self.planeActor )
        self.ren.ResetCamera()
        self.renWin.Render()
        
        
    # ===========================================================
    # Q Callbacks
    # ===========================================================
        
    def WriteScreenShot(self):
        outputFilename = QtWidgets.QFileDialog.getSaveFileName(
                self, 'Save Screenshot As...', 'screenshot.png',
                filter=('*.png'))[0] 
        if ( outputFilename ):
            print ( "Writing:", outputFilename )
            windowToImageFilter = vtk.vtkWindowToImageFilter()
            windowToImageFilter.SetInput( self.renWin )
            windowToImageFilter.Update()
            writer = vtk.vtkPNGWriter()
            writer.SetInputData( windowToImageFilter.GetOutput() )
            writer.SetFileName( outputFilename )
            writer.Write()

# ===============================================	
if __name__ == "__main__": 
    app = QApplication(sys.argv)
    qvtk = SceneViewer()
    # ------------------------------------------- 
    qvtk.GlyphPoints( qvtk.unitSphere, 0.01 )
    qvtk.DisplayLineBetweenTwoPoints( [0,0,0], [0,0,1] )
    qvtk.ren.ResetCamera()
    # -------------------------------------------     
    qvtk.show()
    #sys.exit(app.exec_())
    app.quit()
# ===============================================	
# EOF.