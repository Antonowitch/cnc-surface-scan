# M42.py performs a probing in Z at the current position and
# saves the contact point in the points file.

import sys
# Comment out import only for autocomplete when programming.
# When running the script, the import ___INIT must be removed!!!
# from ___INIT  import *

print("M42 Script gestartet")

# ---------------        Important!!!    ---------------
# Make sure that you have selected the correct probe!
# Konfiguration -> Module -> E/A-Signale

probeIndex = 0
# probeIndex = 1
# probeIndex = 2
# probeIndex = 3
# -------------------------------------------------------

# File to save the 3d points
File_path = gui.scanTXTfilePoints.getText()
try:
    # Open the file to append lines
    File = open(File_path, "a+")
except IOError:
    sys.exit("\n No access to file !!!")

# get machine parameters
Probing_vel = d.getMachineParam(197)
print("Z minus f = " + str(Probing_vel))
Return_vel = d.getMachineParam(196)
print("Z minus f = " + str(Return_vel))
Z_Start = d.getMachineParam(199)
print("Z Start = " + str(Z_Start) )
Z_Ende = d.getMachineParam(200)
print("Z Ende = " + str(Z_Ende) )
Distance = Z_Start -  Z_Ende
print("Z Distance =" + str(Distance) )

# The start position is given by the G-code
Starting_position = d.getPosition(CoordMode.Program)

Maximum_position = Starting_position.copy()
Maximum_position[2] -= Distance

# Perform a probing in Z from the starting point to maximum starting point z minus distance.
# If no contact has occurred on this distance, then the method returns false, otherwise true.
if (d.executeProbing(CoordMode.Program, Maximum_position, probeIndex, Probing_vel) == False):
    # no contact
    d.moveToPosition(CoordMode.Program, Starting_position, Return_vel)
    Saved_text = "Probing Failed !!! \n"
else:
    # contact
    d.moveToPosition(CoordMode.Program, Starting_position, Return_vel)
    # Get the coordinates of the last touch point
    Probe_position = d.getProbingPosition(CoordMode.Program)
    # Store the x, y and Z coordinates of the contact point in the string Saved_text, separated by commas.
    Saved_text = str(Probe_position[0]) + "," + str(Probe_position[1]) + "," + str(Probe_position[2]) + "\n"

try:
    # Write the line Saved_Text into the file
    File.write(Saved_text)
except IOError:
    File.close()
    sys.exit("\n File write error !!!")
    