#******************************************************************************************************
# Created: Dzmitry Ivanou        
# Last Updated: 2023
# Version: 2021.0.1
#
#******************************************************************************************************
# MODIFY THIS AT YOUR OWN RISK

import os
import sys
import importlib
from PySide2 import QtWidgets, QtCore, QtGui
from pymxs import runtime as rt


import at_gen_gui as atgengui
importlib.reload (atgengui)

import at_tabs_gui as attabsgui
importlib.reload (attabsgui)

#import modules
import art_tools as at

#setMaxW
maxWidth = (at.scaledWidth*0.97)

rootDir = ".."

#check root dir
if rootDir not in sys.path:
  sys.path.append( rootDir )

#import pt_config_loader as cfgl
#importlib.reload(cfgl)

class ATWINDOW (QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        
        super(ATWINDOW, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('3D Art Tools 2023')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        #main layout
        self.MainLayout = parent.layout()

        mainVLayout = QtWidgets.QVBoxLayout()

        #tab widget    
        tabAT = QtWidgets.QTabWidget()
        tabAT.setObjectName("tabAT")
        
        #min max size
        tabAT.setMaximumWidth(maxWidth)  
        
        #add tabs
        tabGEN = attabsgui.AT_GEN_TAB()
        tabTEX = attabsgui.AT_TEX_TAB()
        tabUV = attabsgui.AT_UV_TAB()
        tabTOOLS = attabsgui.AT_TOOLS_TAB()
        tabCHECK = attabsgui.AT_CHECK_TAB()
        tabSET = attabsgui.AT_SET_TAB()
        
            
        tabAT.addTab(tabGEN, "General")
        tabAT.addTab(tabTEX, "Texel")
        tabAT.addTab(tabUV, "UV")
        tabAT.addTab(tabTOOLS, "Tools")
        tabAT.addTab(tabCHECK, "Checker")
        tabAT.addTab(tabSET, "Settings")

        #add widgets to main layout
        mainVLayout.addWidget(tabAT)
          
        atWidget = QtWidgets.QWidget()
        atWidget.setLayout(mainVLayout)
        self.setWidget(atWidget)

    def run(self):
        return self

    #delete procedures    
    def __del__(self):
        
        #print ('\n', "PolygonTools cleanup operations...")
        
        #unreg viewport functions
        #rt.unregisterRedrawViewsCallback(genf.showDimensionInViewport)
        #rt.unregisterRedrawViewsCallback(genf.showDimensionInViewport)

        print ('\n', "PolygonTools was closed.")

class atButton(QtWidgets.QPushButton):
  def __init__(self, Text, Tooltip, parent = None):
    super(atButton, self).__init__()
    self.atButton(Text, Tooltip)
              
  def atButton(self, Text, Tooltip):
    #self.setFlat(True)
    self.setText(Text)
    self.setToolTip(Tooltip)
    self.show()

# horizontal layout   
class rowLayoutHor(QtWidgets.QHBoxLayout):
  def __init__(self, Margin, parent = None):
    super(rowLayoutHor, self).__init__()
    self.rowLayoutHor(Margin)
  
  def rowLayoutHor(self, Margin):
    self.setContentsMargins(Margin, Margin, Margin, Margin)

# vertical layout  
class rowLayoutVert(QtWidgets.QVBoxLayout):
  def __init__(self, Margin, parent = None):
    super(rowLayoutVert, self).__init__()
    self.rowLayoutVert(Margin)
  
  def rowLayoutVert(self, Margin):
    self.setContentsMargins(Margin, Margin, Margin, Margin)