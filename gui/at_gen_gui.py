#******************************************************************************************************
# Created: Dzmitry Ivanou        
# Last Updated: 2023
# Version: 2023.0
#
#******************************************************************************************************
# MODIFY THIS AT YOUR OWN RISK

import os
import threading
import sys
from pymxs import runtime as rt


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *

import importlib

#import pt_conclusion as conclusion
#importlib.reload(conclusion)

RootDir = ".."

if RootDir not in sys.path:
  sys.path.append( RootDir )

#import pt_config_loader as cfgl
#importlib.reload(cfgl)

import art_tools as at

import at_gui as atgui
importlib.reload(atgui)

import at_gen_func as atgenf
importlib.reload(atgenf)

maxWidth = (at.scaledWidth*0.97) #set MaxW of window

# set font
font = QFont()
font.setPointSize(11)

#General Tab
class AT_GEN_TAB (QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # Mian Layout
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)

        # Group box for types
        self.cboxCleanupType = QComboBox()
        self.cboxCleanupType.addItems(["Geometry", "Scene", "Viewport", "Butch: G.S.V."])
        self.cboxCleanupType.setToolTip("Choose from list what do you want to cleanup")

        #group box for cleanup options
        self.gboxCleanupOptions = QGroupBox("Cleanup Options")
        self.ClenupOptionsLayout = atgui.rowLayoutVert(4, self)
        self.gboxCleanupOptions.setLayout(self.ClenupOptionsLayout)

        # clenaup button
        self.btnCleanup = atgui.atButton("Cleanup", "Cleanup selected", self)
        
        # Checkbox to poly
        self.cbToEdPoly = QCheckBox()
        self.cbToEdPoly.setText("Convert to Editable Poly")
        self.cbToEdPoly.setToolTip("Convert all selected objects to Editable Poly dyring geometry clenup processing")

         # Checkbox collapse stack
        self.cbCollapseStack = QCheckBox()
        self.cbCollapseStack.setText("Collapse Stack")
        self.cbCollapseStack.setToolTip("Collapse stack for all selected objects dyring geometry clenup processing")

        # to lovercase
        self.cbLowercase = QCheckBox()
        self.cbLowercase.setText("Convert All Names to lowercase")
        self.cbLowercase.setToolTip("Convert all names (meshes, materials) to lowercase for all selected objects dyring geometry clenup processing")

        #convert mat
        self.cbConvertMat = QCheckBox()
        self.cbConvertMat.setText("Convert Materials")
        self.cbConvertMat.setToolTip("Convert materials for all selected objects dyring geometry clenup processing")

        #mat converter cmbox
        self.cboxMaterials = QComboBox()
        self.cboxMaterials.addItems(["Standard (Legasy)", "Physical Material"])
        self.cboxMaterials.setToolTip("Convert all materials in scene to selected type of material")

        #disble comobox mat
        if self.cbConvertMat.isChecked() == False:
          self.cboxMaterials.setEnabled(False)
 
        # Stat button
        self.btnGetStat = atgui.atButton("Get Statistics", "Get statistics for selected geometry", self)

        #Dimension
        self.btnShowDim = atgui.atButton("Show Dimension", "Show bounding box with dimensions for selected objects", self)

        #group box for stat options
        self.gboxStatOptions = QGroupBox("Statistics Options")
        self.StatOptionsLayout = atgui.rowLayoutVert(4, self)
        self.gboxStatOptions.setLayout(self.StatOptionsLayout)
        
        # Stat options
        self.btnZeroSGSel = atgui.atButton("Highlight Zero SG", "Select polygons without smoothing groups", self)
        
        self.btnMergeSGSel = atgui.atButton("Highlight Merged SG", "Select polygons with merged smoothing groups", self)
        
        #Info text here
        self.tbLog = QTextBrowser()
        self.tbLog.setMinimumWidth(maxWidth/2)
        self.tbLog.setFont(font)

        markdownstart = "<h1>3D Art Tools</h1>" \
          "<b>Documentation: </b><br>" \
            "Links: "
        
        self.tbLog.setText(markdownstart)
        
        # Columns layout L and R
        self.LeftColumn = QVBoxLayout()  
        self.LeftColumn.setAlignment(Qt.AlignTop)

        self.RightColumn = QVBoxLayout()
        self.RightColumn.setAlignment(Qt.AlignTop)
        self.RightColumn.setContentsMargins(4, 4, 4, 4)
        
        # Rows for elements
        self.Row01 = atgui.rowLayoutHor(4, self)  
        self.Row02 = atgui.rowLayoutVert(4, self)  
        self.Row03 = atgui.rowLayoutHor(4, self)   
        self.Row04 = atgui.rowLayoutHor(4, self)   
        self.Row05 = atgui.rowLayoutHor(4, self) 
     
        # add layouts Land R to main
        self.mainLayout.addLayout(self.LeftColumn)
        self.mainLayout.addLayout(self.RightColumn)
        
        #add row to column
        self.LeftColumn.addLayout(self.Row01)
        self.LeftColumn.addLayout(self.Row02)
        self.LeftColumn.addLayout(self.Row03)
        self.LeftColumn.addLayout(self.Row04)
        self.LeftColumn.addLayout(self.Row05)

        # Add prepare buttons Row1
        self.Row01.addWidget(self.cboxCleanupType)
        self.Row01.addWidget(self.btnCleanup)

        # Add group box
        self.Row02.addWidget(self.gboxCleanupOptions)
        # Add options
        self.ClenupOptionsLayout.addWidget(self.cbToEdPoly)
        self.ClenupOptionsLayout.addWidget(self.cbCollapseStack)
        self.ClenupOptionsLayout.addWidget(self.cbLowercase)
        self.ClenupOptionsLayout.addWidget(self.cbConvertMat)
        self.ClenupOptionsLayout.addWidget(self.cboxMaterials)

        # Add prepare buttons Row3
        self.Row03.addWidget(self.btnGetStat)
        
        # Add element Row4
        self.Row04.addWidget(self.gboxStatOptions)   
        self.StatOptionsLayout.addWidget(self.btnZeroSGSel)
        self.StatOptionsLayout.addWidget(self.btnMergeSGSel)

        # Add element Row5
        self.Row05.addWidget(self.btnShowDim)
        
        #Right column elements
        self.RightColumn.addWidget(self.tbLog)
        
        #State
        self.btnMergeSGSel.setEnabled(False)
        self.btnZeroSGSel.setEnabled(False)
        
        # Signals
        # Buttons
        self.btnCleanup.clicked.connect(self.btnCleanupClicked)
        self.btnGetStat.clicked.connect(self.btnGetStatClicked)
        self.btnShowDim.clicked.connect(self.btnShowDimClicked)
        self.btnZeroSGSel.clicked.connect(self.btnZeroSGSelClicked)
        self.btnMergeSGSel.clicked.connect(self.btnMergeSGSelClicked)
        
        # check boxes
        self.cbConvertMat.clicked.connect(self.cbConvertMatClicked)
        
        # Combo boxes
        self.cboxCleanupType.activated.connect(self.cbCleanupTypeActivated)

    # turn Material dropbox on or off
    def cbConvertMatClicked(self):
      if self.cbConvertMat.isChecked() == False:
          self.cboxMaterials.setEnabled(False)
      else:    
          self.cboxMaterials.setEnabled(True)

    def cbCleanupTypeActivated(self):
      if self.cboxCleanupType.currentIndex() == 2:
        self.gboxCleanupOptions.setEnabled(False)
      else:
        self.gboxCleanupOptions.setEnabled(True)

    def btnCleanupClicked(self):

      TOLOWERCASE = self.cbLowercase.isChecked()
      TOEPOLY = self.cbToEdPoly.isChecked()
      COLLAPSESTACK = self.cbCollapseStack.isChecked()

      CLEANUPTYPE = self.cboxCleanupType.currentIndex()

      if CLEANUPTYPE == 0:
        self.geometryClaenup(TOLOWERCASE, TOEPOLY, COLLAPSESTACK)

      
    
    def geometryClaenup(self, TOLOWERCASE, TOEPOLY, COLLAPSESTACK):

      self.tbLog.setMarkdown("### Geometry Cleanup Statistics")

      # Run check names
      name_check_result = atgenf.nameChecker(TOLOWERCASE)
      
      # Run check Selection  
      check_result = atgenf.checkSelection(TOEPOLY, COLLAPSESTACK)
      
      sel_objects = check_result[0]
      sel_editable_poly_objects = check_result[1]
      sel_bones = check_result[2]
      sel_editable_poly_nodes = check_result[3]
      messages = check_result[4]

      # stat selection
      SelectedObjects = len(sel_objects)
      SelectedEditablePolyObj = len(sel_editable_poly_objects)
      SelectedBones = len(sel_bones)

      self.tbLog.append("Selected objects: " + str(SelectedObjects))

      self.tbLog.append("Editable Poly objects: " + str(SelectedEditablePolyObj))

      self.tbLog.append("Bones: " + str(SelectedBones))

      self.tbLog.append("--")

      for i in range(len(messages)):
        self.tbLog.append(messages[i])
                
      rt.redrawViews()

      if len(sel_editable_poly_objects) > 0:

        scene_name_data = atgenf.sceneName()
        self.tbLog.append(scene_name_data[1])

        # Run Prepare mesh
        check_data = atgenf.prepareMesh(sel_editable_poly_objects)

        prep_messages = check_data[1]

        for i in range(len(prep_messages)):
          self.tbLog.append(prep_messages[i])
 
    
    
    def btnGetStatClicked(self):
     self.tbLog.setMarkdown("Statistics")
     
    def btnShowDimClicked(self):
     self.tbLog.setMarkdown("Dimension")

    def btnZeroSGSelClicked(self):
     self.tbLog.setMarkdown("Zero SG")
     
    def btnMergeSGSelClicked(self):
     self.tbLog.setMarkdown("Dimension")