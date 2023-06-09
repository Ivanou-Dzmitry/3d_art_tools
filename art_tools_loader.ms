--******************************************************************************************************	
-- Last Updated: 2023
-- Dzmitry Ivanou
--******************************************************************************************************
-- MODIFY THIS AT YOUR OWN RISK


macroScript ArtTools3D
 category:"3D Art Tools"
 tooltip:"3D Art Tools 2023"
 buttonText:"3D Art Tools"
 Icon: #("art_tools_32", 1)

(

scriptsDir = getDir #scripts
userScriptsDir = getDir #userScripts 
userIconsDir = getDir #userIcons

-- Main Module File Name
mainModule = userScriptsDir + "\3d_art_tools\art_tools.py"

--Execute Main Module
python.ExecuteFile mainModule

)