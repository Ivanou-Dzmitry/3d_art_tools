#*****************************
# Created: Dzmitry Ivanou        
# Last Updated: 2023
# Version: 2023.0
#*****************************
# MODIFY THIS AT YOUR OWN RISK

import sys
import os
import random
import string
import importlib
from pymxs import runtime as rt

import at_gen_gui as atgengui
importlib.reload(atgengui)
    
def checkSelection(ToPoly, CollapseStack):
    
    #arrays for objects
    all_sel_obj = []
    editable_poly_obj = []
    bones_obj = []

    editable_poly_nodes = []
    other_nodes = []
    messages = []

    #selected obj
    SelObjCount = rt.selection.count
    
    if SelObjCount > 0:
        
        #get selected nodes
        SelectedNodes = rt.selection
        
        for c in SelectedNodes:
            
            ObjectName = str(c.name)

            #all selected objects     
            all_sel_obj.append(ObjectName)

            #If Collapse True IMPORTANT!
            if CollapseStack==True:
                rt.maxops.collapsenode((c), True)

            #Ic Convert to Poly is true IMPORTANT!
            if ToPoly==True:
                rt.convertToPoly (c)

            #get class names
            ObjectType = str(rt.classOf(c))

            if ObjectType == "Editable_Poly":
                editable_poly_obj.append(ObjectName)
                editable_poly_nodes.append(c)            
            #bones
            elif ObjectType == "BoneGeometry":
                bones_obj.append(ObjectName)		
                other_nodes.append(c)
            else:
                other_nodes.append(c)       

            # deselect other nodes
            if len(other_nodes) > 0:
                for i in range(len(other_nodes)):
                    rt.deselect (other_nodes[i])   
                                  
    else:
        messages.append("Please select something!")


    messages.append("Complete!")

    return all_sel_obj, editable_poly_obj, bones_obj, editable_poly_nodes, messages


def nameChecker(ToLowercase):
    
    NewName = ""
    Message = ""
    Renamed = False

    SelectedNodes = rt.selection
        
    for c in SelectedNodes:

        OldName = str(c.name)
     
        # Random letter
        RandomLetter = ''.join([random.choice(string.ascii_letters) for n in range(1)])
        RandomNumber = str(random.randrange(1, 1000))
 
        if len(OldName) == 0:
            #add random rename
            NewName = "renamed_object_" + RandomLetter + RandomNumber
            c.name = NewName
            Message = ("Object was renamed during processing because the object didn't have a name. New name: " + NewName)
            Renamed = True
        elif "\'" in OldName:
            NewName = OldName.replace("\'", "")
            c.name = NewName
            Message = ("Object was renamed during processing because the object had invalid characters in the name. New name: " + NewName)
            Renamed = True
        elif ToLowercase == True:
            NewName = OldName.lower()
            c.name = NewName
            Renamed = True
        else:
            NewName = OldName
            Renamed = False
            
    return NewName, Message, Renamed

def sceneName():

    #scene_name_conclusion_data = False   

    Message = ""

    #get path and name
    PathToCurrentFile = rt.maxFilePath
    MaxFileName = rt.maxFileName
    #MaxFileName = rt.getFilenameFile(rt.maxFileName)

    #abs path
    AbsolutePathToScene = PathToCurrentFile + MaxFileName

    #path yes or not
    if PathToCurrentFile == "":
        Message = "Please save current scene!"
    else:
        Message = "Current file name is: " + AbsolutePathToScene

    return AbsolutePathToScene, Message

def prepareMesh(sel_editable_poly_objects):

    prep_mesh_conclusion_data = []
    messages = []

    # STEP 1: unhide layers
    try:
        for i in range(0, rt.LayerManager.count):
            rt.LayerManager.getLayer(i).on = True

        rt.execute ("max unhide all")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    # STEP 2: Unfreeze All
    try:
        rt.execute ("max unfreeze all")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    # STEP 3 Clear Slots
    try:
        rt.execute ("macros.run \"Medit Tools\" \"clear_medit_slots\"")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    # STEP 4 - Unhide Faces
    try:
        for i in range(len(sel_editable_poly_objects)):
            rt.execute ("$" + sel_editable_poly_objects[i] + ".EditablePoly.unhideAll #Face")
        prep_mesh_conclusion_data.append(True)
    except:
        print ("Faces Unhiden not supported for current type of the object! Object Name:", sel_editable_poly_objects[i])
        prep_mesh_conclusion_data.append(False)

    # STEP 5 - Unhide Vertex
    try:
        for i in range(len(sel_editable_poly_objects)):
            rt.execute ("$" + sel_editable_poly_objects[i] + ".EditablePoly.unhideAll #Vertex")
        prep_mesh_conclusion_data.append(True)
    except:
        print ("Vertices Unhiden not supported for current type of the object! Object Name:", sel_editable_poly_objects[i])
        prep_mesh_conclusion_data.append(False)

    # STEP 6 ResetX Form
    try:
        for i in range(len(sel_editable_poly_objects)):
            rt.execute ("resetxform $" + sel_editable_poly_objects[i])
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    # STEP 7 Convert to poly
    try:
        for i in range(len(sel_editable_poly_objects)):
            rt.execute ("convertto $" + sel_editable_poly_objects[i] + " editable_poly")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    # STEP 8 BackfaceON
    try:
        for i in range(len(sel_editable_poly_objects)):
            rt.execute ("$" + sel_editable_poly_objects[i] + ".backfacecull = true")
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    fixed_material_obj = []
    assigned_material_obj = []

    # STEP 9
    try:
        for i in range(len(sel_editable_poly_objects)):
            
            #GET MAT BY OBJECT
            ObjectName = sel_editable_poly_objects[i]                
            NodeName = rt.getNodeByName(ObjectName)
            CurrentMat = NodeName.material       

            #try to get mat
            try:
                #get mat class
                MaterialClass = str(rt.classOf(CurrentMat))
   
                #get mat name
                MaterialName =  str(NodeName.material.name)

            except:

                #no mat assigned
                MaterialClass = "None"
                MaterialName = "None"

            # if no materials assigned
            if MaterialClass == "None" and MaterialName == "None":
                rt.execute ("$" + sel_editable_poly_objects[i] + ".material = PhysicalMaterial()")
                rt.execute ("$" + sel_editable_poly_objects[i] + ".material.name = $" + sel_editable_poly_objects[i] + ".name + \"_mat\"")
                assigned_material_obj.append(sel_editable_poly_objects[i] )
        
            #fix default names
            if ("- Default" in MaterialName) or ("Material #" in MaterialName) or (len(MaterialName) == 0):                     
                rt.execute ("$" + sel_editable_poly_objects[i] + ".material.name = $" + sel_editable_poly_objects[i] + ".name + \"_mat\"")
                fixed_material_obj.append(sel_editable_poly_objects[i] )

            # if it multi sub object
            if MaterialClass == "Multimaterial":
                
                MaterialsList = NodeName.material.materialList
                
                for k in range(len(MaterialsList)):
                    
                    #get sub mat
                    SubMaterial = MaterialsList[k]
                    
                    if SubMaterial != None:

                        SubMatClass = rt.classOf(MaterialsList[k])
                        SubMatName = str(SubMaterial.name)

                        if ("- Default" in SubMatName) or ("Material #" in SubMatName) or (len(SubMatName) == 0):

                            NewMatName = sel_editable_poly_objects[i] + "_ID" + str(k+1)
                            SubMaterial.name = NewMatName
                            
                            #add only unique
                            if sel_editable_poly_objects[i] not in fixed_material_obj:
                                fixed_material_obj.append( sel_editable_poly_objects[i] )
                            
        prep_mesh_conclusion_data.append(True)                        
    except:
        prep_mesh_conclusion_data.append(False)    

    #for uniqe mat and objects
    unique_materials = []
    unique_material_obj = []

    #get Unique mats
    try:
        for i in range(len(sel_editable_poly_objects)):
            
            ObjectName = sel_editable_poly_objects[i]  
            NodeName = rt.getNodeByName( ObjectName )
            MaterialName =  NodeName.material.name

            if MaterialName not in unique_materials:                
                unique_materials.append(MaterialName)
                unique_material_obj.append(NodeName)
    except:
        print ("Can't collect unique Materials. Error 1 in 'prepareMesh' function.")

    #add Mats to Slots
    try:
        for i in range(len(unique_material_obj)):            
            rt.meditMaterials[i] = unique_material_obj[i].material
    except:
        print ("Can't update Material slots! Error 2 in 'prepareMesh' function.")

    #STEP 10 -- turnoff vertex color
    for i in range(len(sel_editable_poly_objects)):
        rt.execute ("$" + sel_editable_poly_objects[i] + ".showVertexColors = off")

    # Redraw viewport
    try:
        rt.redrawViews()
        prep_mesh_conclusion_data.append(True)
    except:
        prep_mesh_conclusion_data.append(False)

    #0
    if prep_mesh_conclusion_data[0] == True:
        messages.append("1. All objects and Layers are Unhidden.")
    #1
    if prep_mesh_conclusion_data[1] == True:
        messages.append("2. All objects are Unfrozen.")
    #2
    if prep_mesh_conclusion_data[2] == True:
        messages.append("3. Material Slot Reseted."        )
    #3    
    if prep_mesh_conclusion_data[3] == True:
        messages.append("4. All Faces are Unhidden.")
    #4    
    if prep_mesh_conclusion_data[4] == True:
        messages.append("5. All Vertices are Unhidden.")
    #5    
    if prep_mesh_conclusion_data[5] == True:
        messages.append("6. Reset XForm applied to all objects.")
    #6    
    if prep_mesh_conclusion_data[6] == True:
        messages.append("7. All objects are converted to Editable Poly.")
    #7    
    if prep_mesh_conclusion_data[7] == True:
        messages.append("8. Backface Cull in ON for all objects.")
    #8    
    if prep_mesh_conclusion_data[8] == True:
        messages.append("9. Materials was processed.")
    

    #print(prep_mesh_conclusion_data)

    return prep_mesh_conclusion_data, messages