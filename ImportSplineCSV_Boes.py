#Author- Bös
#Description- Generate Splines, the Splines lofted to a surface


import adsk.core, adsk.fusion, traceback
import io

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        # Get all components in the active design.
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        title = 'Import Spline csv'
        if not design:
            ui.messageBox('No active Fusion design', title)
            return
        
        dlg = ui.createFileDialog()
        dlg.title = 'Open CSV File'
        dlg.filter = 'Comma Separated Values (*.csv);;All Files (*.*)'
        if dlg.showOpen() != adsk.core.DialogResults.DialogOK :
            return
        
        filename = dlg.filename
        with io.open(filename, 'r', encoding='utf-8-sig') as f:
            points = adsk.core.ObjectCollection.create()
            splines = adsk.core.ObjectCollection.create()
            line = f.readline()
            data = []
            while line:
                pntStrArr = line.split(',')
                for pntStr in pntStrArr:
                    try:
                        data.append(float(pntStr))
                    except:
                        break
            
                if len(data) >= 3 :
                    point = adsk.core.Point3D.create(data[0], data[1], data[2])
                    points.add(point)
                data.clear() 
                line = f.readline()
               # ui.messageBox(line)
                if line.startswith('createSpline'):
                    #ui.messageBox("Create Spline")
                    #root = design.rootComponent     
                    splines.add(sketch.sketchCurves.sketchFittedSplines.add(points))
                    points.clear()
                    line = f.readline()        
        # Create loft feature input
        loftFeats = rootComp.features.loftFeatures
        loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        loftSectionsObj = loftInput.loftSections
        for spline in splines:
            loftSectionsObj.add(spline)
        loftInput.isSolid = False
        loftInput.isClosed = False
        loftInput.isTangentEdgesMerged = True

        # Create loft feature
        loftFeats.add(loftInput)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

