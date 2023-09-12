
# gen function processing
def genProcessor(result_data):

    messages = []

    if result_data[0] == True:
        messages.append("1. All objects and Layers are Unhidden.")
    else:
        messages.append("1. Problems with Unhidden.")

    #1
    if result_data[1] == True:
        messages.append("2. All objects are Unfrozen.")
    else:
        messages.append("2. Problems with Unfrozen.")    
    #2
    if result_data[2] == True:
        messages.append("3. Material slot was reseted.")
    else:
        messages.append("2. Problems with material slot reset.")            
    #3    
    if result_data[3] == True:
        messages.append("4. All Faces are Unhidden.")
    else:
        messages.append("ERROR!") 
    #4    
    if result_data[4] == True:
        messages.append("5. All Vertices are Unhidden.")
    else:
        messages.append("ERROR!") 
    #5    
    if result_data[5] == True:
        messages.append("6. Reset XForm procedure was applied to all objects.")
    else:
        messages.append("ERROR!") 
    #6    
    if result_data[6] == True:
        messages.append("7. All objects are converted to Editable Poly.")
    else:
        messages.append("ERROR!") 
    #7    
    if result_data[7] == True:
        messages.append("8. Backface Cull is ON for all objects.")
    else:
        messages.append("ERROR!") 
    #8    
    if result_data[8] == True:
        messages.append("9. Materials was processed.")
    else:
        messages.append("ERROR!") 

    return messages