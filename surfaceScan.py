import math
import sys


xStart = d.getMachineParam(190)
xEnde = d.getMachineParam(191)
if xEnde < xStart:
    temp = xEnde
    xEnde = xStart
    xStart = temp
print("xStart = " +str(xStart) )
print("xEnde = " +str(xEnde) )
xDelta = abs(xStart - xEnde)
#print("Delta X = "  + str(xDelta))
xAnzahlPunkte = d.getMachineParam(192)
#print("Anzahl Punkte x = " +str(xAnzahlPunkte) )

yStart = d.getMachineParam(193)
yEnde = d.getMachineParam(194)
if yEnde < yStart:
    temp = yEnde
    yEnde = yStart
    yStart = temp

#print("yStart = " +str(yStart) )
#print("yEnde = " +str(yEnde) )
yDelta = abs(yStart - yEnde)
#print("Delta Y = "  + str(yDelta))
yAnzahlPunkte = d.getMachineParam(195)
#print("Anzahl Punkte y = " +str(yAnzahlPunkte) )

sichereHoehe = d.getMachineParam(199)
#print("Sichere Höhe = " + str(sichereHoehe))

vorschubXY =  d.getMachineParam(198)
#print("Voschub XY = " + str(vorschubXY))

vorschubZplus =  d.getMachineParam(196)
#print("Voschub Zplus = " + str(vorschubZplus))

x=xStart
y=yStart
G_Code = "G90 G17 G80\n"
G_Code += "G21\n" #Unit mm
G_Code += "G90 G49\n"  #Tool length compensation off

#go to Startposition
G_Code += "G01 Z" + str(sichereHoehe) + " F"+str(vorschubZplus)+"\n"
G_Code += "G01 x"+str(xStart) + " y" + str(yStart) + " F"+str(vorschubXY)+"\n"

counterX = 0;
counterY = 0;


while x <= xEnde:
    while y <= yEnde:
        G_Code += "M42\n"
        counterY +=1;
        y= yStart + counterY * yDelta / (yAnzahlPunkte - 1)
        if y <= yEnde: #nicht in y weiterfahren, wenn yEnde erreicht
            G_Code += "G01 Y"+ str(y) + "  F" + str(vorschubXY)+"\n"
    G_Code +="M43 \n" #M43 write createSpline to File
    y=yStart
    counterY = 0
    counterX += 1;
    x = xStart + counterX * xDelta / (xAnzahlPunkte -1)
    if x <= xEnde: #nicht in x weiterfahren, falls xEnde erreicht
        G_Code += "G01 Y" + str(y) +"\n"
        print("x=" + str(x))
        G_Code += "G01 X" + str(x) + " F" + str(vorschubXY)+"\n"

# Filepath for points.csv
File_path_points = gui.scanTXTfilePoints.getText() ;
# Filepath for G-Code
File_path_G_Code = gui.scanTXTfileGcode.getText() ;

try:
    File_GCode = open(File_path_G_Code, "w+")
    #Create File points.csv or override points.csv
    File_Points = open(File_path_points,"w")
except IOError:
    sys.exit("\n No access to file !!!\n" + File_path_G_Code)

# Write String G_Code to file
try:
    File_GCode.write(G_Code)
    File_GCode.close()
    # load G-Code from file
    d.openGCodeFile(File_path_G_Code)
    print("---     CNC program successfully created!      ---")
    print(">>>  click on Yes (reload G-code) <<<\n")

except IOError:
    File_GCode.close()
    File_path_points.close()
    sys.exit("\n File write error !!!")

#print(G_Code)
