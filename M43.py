# M43.py is called at the end of a scan line and
# writes only one line ("createSpline") to the points file

print("Create Spline\n")

File_path = gui.scanTXTfilePoints.getText()

# File to save the 3d points
try:
    # Open the file to append lines
    File = open(File_path, "a+")
    File.write("createSpline")
except IOError:
    sys.exit("\n No access to file !!!")