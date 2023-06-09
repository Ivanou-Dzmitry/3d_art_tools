#******************************************************************************************************
# Created: Dzmitry Ivanou        
# Last Updated: 2023
# Version: 2021.0.1
#
#******************************************************************************************************
# MODIFY THIS AT YOUR OWN RISK

import os
import sys
import math 
from pymxs import runtime as rt
import random
import importlib

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *

import pt_conclusion as conclusion
importlib.reload(conclusion)

import pt_conclusion as conclusion
importlib.reload(conclusion)

import pt_gen_func as gen_func
importlib.reload(gen_func)

import pt_uv_func as uvf
importlib.reload (uvf)

RootDir = ".."

if RootDir not in sys.path:
  sys.path.append( RootDir )
  
import pt_config_loader as cfgl
importlib.reload(cfgl)

import polygon_tools as pt

maxWidth = (pt.scaledWidth*0.97)

#GUI    
class PT_Toools_Tab (QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        
        #set layot
        self.tabTool_v_layout = QVBoxLayout(self)
        self.tabTool_v_layout.setAlignment(Qt.AlignTop)