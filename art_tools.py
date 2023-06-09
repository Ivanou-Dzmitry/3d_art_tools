#******************************************************************************************************
# Created: Dzmitry Ivanou        
# Last Updated: 2023
# Version: 2023
#
#******************************************************************************************************
# MODIFY THIS AT YOUR OWN RISK

import os
import sys
import importlib
import qtmax
from PySide2 import QtWidgets, QtCore, QtGui
from pymxs import runtime as rt

#intitial for 100%
iWidth = 640
iHeight = 480

#get scaling
scaleCoef = rt.GetUIScaleFactor()

#new dimension
scaledWidth = iWidth*scaleCoef
scaledHeight = iHeight*scaleCoef

#add Paths
tempCurrentDir = os.path.dirname(__file__)
currentDir = tempCurrentDir.replace ("\\", "/")

#path to config file
tempGUIPath = (currentDir + "\\gui")
guiPath = tempGUIPath.replace ("\\", "/")

#path to config file
tempFuncPath = (currentDir + "\\functions")
funcPath = tempFuncPath.replace ("\\", "/")

#add path
if currentDir not in sys.path:
  sys.path.append( currentDir )

if guiPath not in sys.path:
  sys.path.append( guiPath )
  
if funcPath not in sys.path:
  sys.path.append( funcPath )
  
#pt files
import at_gui as atgui
importlib.reload(atgui)
  
def main():    
    #get main window
    mainWindow = qtmax.GetQMaxMainWindow()

    #create ptgui
    appWindow = atgui.ATWINDOW(parent = mainWindow)

    #set, resize and show
    appWindow.setFloating(True)
    appWindow.resize(scaledWidth, scaledHeight)
    appWindow.show()    

if __name__ == '__main__':
	main()    
