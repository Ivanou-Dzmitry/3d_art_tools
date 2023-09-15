#*****************************
# Created: Dzmitry Ivanou        
# Last Updated: 2023
# Version: 2023.0
#*****************************
# MODIFY THIS AT YOUR OWN RISK

import sys
import os
import re
import random
import string
import importlib
from pymxs import runtime as rt

sys.dont_write_bytecode = True

#for debug print
DebugPrint = True

def Cleanup(TOLOWERCASE, TOEPOLY, COLLAPSESTACK):

    cleanup_message = []
    cleanup_message.append("CLEANUP SUMMARY")

    #First we check names and reneme if necessary
    name_check_result = []
    name_check_result = nameChecker(TOLOWERCASE)
    
    #add info to summary
    if name_check_result[1] == True:
        renamedObjectsCount = (len(name_check_result[0]))
        cleanup_message.append("\nRenamed objects (" + str(renamedObjectsCount) + "):")
        for i in range(len(name_check_result[0])):
            cleanup_message.append(name_check_result[0][i])
   
    # Second we check geometry and stack
    check_result = []
    check_result = checkSelection(TOEPOLY, COLLAPSESTACK)

    sel_objects = check_result[0]
    sel_editable_poly_objects = check_result[1]
    sel_bones = check_result[2]
    sel_editable_poly_nodes = check_result[3]

    if len(check_result[4]) > 0:
        objectsConvertedToPoly = (len(check_result[4]))
        cleanup_message.append("\nObjects Converted To Poly (" + str(objectsConvertedToPoly) + "):")
        for i in range(len(check_result[4])):
            cleanup_message.append(check_result[4][i])

    if len(check_result[5]) > 0:
        objectsCollapsed = (len(check_result[5]))
        cleanup_message.append("\nCollapsed Objects (" + str(objectsCollapsed) + "):")
        for i in range(len(check_result[5])):
            cleanup_message.append(check_result[5][i])

    # stat selection
    SelectedObjects = len(sel_objects)
    SelectedEditablePolyObj = len(sel_editable_poly_objects)
    SelectedBones = len(sel_bones)

    # Run Prepare mesh
    check_data = []
    if len(sel_editable_poly_objects) > 0:
        check_data = prepareMesh(sel_editable_poly_objects)

        editablePolyObjects = (len(sel_editable_poly_objects))
        cleanup_message.append("\nProceeded Objects List (" + str(editablePolyObjects) + "):")
        for i in range(len(sel_editable_poly_objects)):
            cleanup_message.append(sel_editable_poly_objects[i])

        cleanup_message.append("\nOperations Performed:")
        for i in range(len(check_data[1])):
            cleanup_message.append(check_data[1][i])
    else:
        cleanup_message.append("\nCleanup was not done. Possible reasons:\nNo objects of type editable poly were selected. Geometry cleanup works only with editable poly objects.\nIs the stack of your objects collapsed?")
        check_data.append("null")
        check_data.append("null")
        
    if DebugPrint == True:
        print("-- prepareMesh --")
        print("Data for conclusion:", check_data[0])
        print("Cleanup Items:", check_data[1])

    if DebugPrint == True:
        print("-- Cleanup Message --")
        for i in range(len(cleanup_message)):
            print(cleanup_message[i])
    
    return check_data, cleanup_message


def checkSelection(ToPoly, CollapseStack):
    
    #arrays for objects
    all_sel_obj = []
    editable_poly_obj = []
    bones_obj = []

    editable_poly_nodes = []
    other_nodes = []

    converted_objects = []
    collapsed_objects = []

    #selected obj
    SelObjCount = rt.selection.count
    
    if SelObjCount > 0:
        
        #get selected nodes
        SelectedNodes = rt.selection
        
        for c in SelectedNodes:
            
            ObjectName = str(c.name)

            #all selected objects     
            all_sel_obj.append(ObjectName)

            #count modifiers in stack
            modifiersCount = len(c.modifiers)

            #If Collapse True and obj has stack IMPORTANT!
            if (CollapseStack == True and modifiersCount > 0):
                rt.maxops.collapsenode((c), True)
                collapsed_objects.append(ObjectName)

            #Ic Convert to Poly is true and hasnt stack and no edit poly IMPORTANT!
            if ((ToPoly == True) and (str(rt.classOf(c)) != "Editable_Poly") and modifiersCount == 0):
                rt.convertToPoly (c)
                converted_objects.append(ObjectName)

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

    if DebugPrint == True:
        print("-- checkSelection --")
        print ("sel_objects:", all_sel_obj)
        print ("sel_editable_poly_objects:", editable_poly_obj)
        print ("sel_bones:", bones_obj)
        print ("sel_editable_poly_nodes:", editable_poly_nodes)
        print ("converted_objects:", converted_objects)
        print ("collapsed_objects:", collapsed_objects)

    return all_sel_obj, editable_poly_obj, bones_obj, editable_poly_nodes, converted_objects, collapsed_objects

# Function for check names
def nameChecker(ToLowercase):
    
    NewName = ""
    Message = ""
    Renamed = False
    renamed_objects = []

    # this symbols will be removed from name
    bad_characters = '!@#$%^&*()+?=,\\:;"<>/'

    SelectedNodes = rt.selection
        
    for c in SelectedNodes:

        OldName = str(c.name)
     
        # Random letter
        RandomLetter = ''.join([random.choice(string.ascii_letters) for n in range(1)])
        RandomNumber = str(random.randrange(1, 1000))
 
        if len(OldName) == 0:
            #Fix empty name - add random name
            NewName = "renamed_obj_" + RandomLetter + RandomNumber
            c.name = NewName
            Message = ("The object had no name. New name is " + NewName)
            renamed_objects.append(Message)
            Renamed = True  
        elif any(c in bad_characters for c in OldName):
            #Fix symbols - remove it
            NewName = re.sub('\W+','', OldName)
            if len(NewName) == 0:
                NewName = "renamed_obj_" + RandomLetter + RandomNumber
            c.name = NewName 
            Message = ("Object had invalid characters in the name. Fixed name is " + NewName)
            renamed_objects.append(Message)
            Renamed = True
        elif ToLowercase == True:
            NewName = OldName.lower()
            c.name = NewName
            Renamed = True
        else:
            NewName = OldName
            Renamed = False

        # print to log
        if DebugPrint == True:
            print("-- nameChecker --")
            print("Was Renamed:", Renamed)
            print("Renamed Objects:", renamed_objects)
            
    return renamed_objects, Renamed

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

    return prep_mesh_conclusion_data, messages