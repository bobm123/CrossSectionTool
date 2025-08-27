"""Cross-Section Generator for Fusion 360
Automatically generates cross-sectional sketches from selected bodies along specified axes.
"""

import traceback
import adsk.core
import adsk.fusion

# Global variables
_app = None
_ui = None
_handlers = []

# Event handler for input changes
class CrossSectionInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            inputs = eventArgs.inputs
            changedInput = eventArgs.input
            
            # Handle distribution method change
            if changedInput.id == 'distribution':
                distributionDropdown = inputs.itemById('distribution')
                quantityInput = inputs.itemById('quantity')
                
                if distributionDropdown.selectedItem.name == 'Count':
                    quantityInput.unitType = ''
                    quantityInput.value = 6
                    quantityInput.minimumValue = 1
                    quantityInput.maximumValue = 100
                else:  # Distance
                    quantityInput.unitType = 'cm'
                    quantityInput.value = 5.0
                    quantityInput.minimumValue = 0.1
                    quantityInput.maximumValue = 1000.0
                    
            # Update OK button state
            updateOkButtonState(inputs)
            
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Event handler for command destruction
class CrossSectionDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            adsk.terminate()
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Event handler for command execution
class CrossSectionExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            command = adsk.core.Command.cast(args.command)
            inputs = command.commandInputs
            
            # Get input values
            bodiesInput = inputs.itemById('bodies')
            axisInput = inputs.itemById('axis') 
            distributionInput = inputs.itemById('distribution')
            suppressionInput = inputs.itemById('suppression')
            quantityInput = inputs.itemById('quantity')
            
            # Get input values
            selectedBodies = [bodiesInput.selection(i).entity for i in range(bodiesInput.selectionCount)]
            selectedAxis = axisInput.selection(0).entity if axisInput.selectionCount > 0 else None
            distributionMethod = distributionInput.selectedItem.name
            suppressionEnabled = suppressionInput.value
            quantity = int(quantityInput.value) if distributionMethod == 'Count' else quantityInput.value
            
            # Display collected parameters
            message = f"Cross-Section Generation Parameters:\n\n"
            message += f"Bodies: {len(selectedBodies)} selected\n"
            message += f"Axis: {selectedAxis.entityToken if selectedAxis else 'None'}\n" 
            message += f"Distribution: {distributionMethod}\n"
            message += f"Suppression: {suppressionEnabled}\n"
            message += f"Quantity: {quantity}\n\n"
            
            _ui.messageBox(message)
            
            if not selectedBodies or not selectedAxis:
                return
            
            # Get the active design and root component
            app = adsk.core.Application.get()
            design = adsk.fusion.Design.cast(app.activeProduct)
            if not design:
                _ui.messageBox("No active Fusion design")
                return
                
            rootComp = design.rootComponent
            
            # Calculate bounds along the selected axis
            # For simplicity, we'll use a default range - in full implementation,
            # this would analyze the selected bodies' bounds along the axis
            axisLine = selectedAxis.geometry
            axisVector = axisLine.startPoint.vectorTo(axisLine.endPoint)
            axisVector.normalize()
            axisOrigin = axisLine.startPoint
            
            # Create evenly distributed offset planes
            if distributionMethod == 'Count':
                planeCount = quantity
                # Default distribution range (this should be calculated from body bounds)
                startOffset = -10.0  # cm
                endOffset = 10.0     # cm
                
                if planeCount == 1:
                    offsets = [0.0]
                else:
                    offsetRange = endOffset - startOffset
                    offsets = [startOffset + (i * offsetRange / (planeCount - 1)) for i in range(planeCount)]
            else:
                # Distance-based distribution would be implemented here
                planeCount = 6  # Default for now
                offsets = [-10.0 + i * 3.33 for i in range(planeCount)]
            
            # Create construction planes in root component for now
            constructionPlanes = rootComp.constructionPlanes
            createdPlanes = []
            
            # Try creating planes using setByDistanceOnPath with normalized distances (0-1)
            for i, offset in enumerate(offsets):
                try:
                    # Create offset plane input
                    planeInput = constructionPlanes.createInput()
                    
                    # Calculate normalized distance (0-1) along the path
                    # Map our offset range to 0-1 range
                    normalizedDistance = (offset - offsets[0]) / (offsets[-1] - offsets[0]) if len(offsets) > 1 else 0.5
                    # Clamp to 0-1 range
                    normalizedDistance = max(0.0, min(1.0, normalizedDistance))
                    
                    distanceValue = adsk.core.ValueInput.createByReal(normalizedDistance)
                    planeInput.setByDistanceOnPath(selectedAxis, distanceValue)
                    
                    # Create the plane
                    planeFeature = constructionPlanes.add(planeInput)
                    planeFeature.name = f"Section_Plane_{i+1:03d}"
                    
                    createdPlanes.append(planeFeature)
                    
                    if suppressionEnabled:
                        planeFeature.isSuppressed = True
                        
                except Exception as e:
                    _ui.messageBox(f"Failed to create plane {i+1} with distanceOnPath method: {str(e)}")
                    # Fall back to XY plane offset
                    try:
                        planeInput = constructionPlanes.createInput()
                        
                        # Use XY plane as reference with Z offset
                        xyPlane = rootComp.xYConstructionPlane
                        offsetValue = adsk.core.ValueInput.createByReal(offset)
                        planeInput.setByOffset(xyPlane, offsetValue)
                        
                        planeFeature = constructionPlanes.add(planeInput)
                        planeFeature.name = f"Section_Plane_{i+1:03d}"
                        createdPlanes.append(planeFeature)
                        
                        if suppressionEnabled:
                            planeFeature.isSuppressed = True
                            
                    except Exception as e2:
                        _ui.messageBox(f"Failed both distanceOnPath and XY offset methods for plane {i+1}: {str(e2)}")
                        break
            
            _ui.messageBox(f'Successfully created {len(createdPlanes)} construction planes in root component')
            
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Event handler for command creation
class CrossSectionCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            cmd = adsk.core.Command.cast(args.command)
            
            # Connect event handlers
            onDestroy = CrossSectionDestroyHandler()
            cmd.destroy.add(onDestroy)
            _handlers.append(onDestroy)
            
            onInputChanged = CrossSectionInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            _handlers.append(onInputChanged)
            
            onExecute = CrossSectionExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)
            
            # Create the command dialog
            inputs = cmd.commandInputs
            
            # Bodies selection input
            bodiesInput = inputs.addSelectionInput('bodies', 'Bodies', 'Select bodies for cross-section generation')
            bodiesInput.addSelectionFilter('SolidBodies')
            bodiesInput.addSelectionFilter('SurfaceBodies')
            bodiesInput.setSelectionLimits(1, 0)  # At least 1, no upper limit
            
            # Axis selection input  
            axisInput = inputs.addSelectionInput('axis', 'Axis', 'Select axis')
            #axisInput.addSelectionFilter('ConstructionAxes')
            axisInput.setSelectionLimits(1, 1)  # Exactly 1
            
            # Distribution method dropdown
            distributionInput = inputs.addDropDownCommandInput('distribution', 'Distribution', adsk.core.DropDownStyles.TextListDropDownStyle)
            distributionItems = distributionInput.listItems
            distributionItems.add('Count', True)  # Default selection
            distributionItems.add('Distance', False)
            
            # Suppression checkbox
            suppressionInput = inputs.addBoolValueInput('suppression', 'Suppression', True, '', False)
            
            # Quantity input (initially as count)
            quantityInput = inputs.addIntegerSpinnerCommandInput('quantity', 'Quantity', 1, 100, 1, 6)
            
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def updateOkButtonState(inputs):
    """Update the OK button enabled state based on input validation"""
    try:
        bodiesInput = inputs.itemById('bodies')
        axisInput = inputs.itemById('axis')
        
        # Enable OK if we have at least one body and one axis selected
        isValid = bodiesInput.selectionCount > 0 and axisInput.selectionCount > 0
        
        # Note: In actual Fusion 360 API, the OK button state is managed automatically
        # based on required inputs, but this shows the validation logic
        
    except:
        pass

def run(_context: str):
    """Main entry point for the script"""
    try:
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui = _app.userInterface
        
        # Create command definition
        cmdDef = _ui.commandDefinitions.itemById('crossSectionGenerator')
        if not cmdDef:
            cmdDef = _ui.commandDefinitions.addButtonDefinition(
                'crossSectionGenerator', 
                'Cross-Section Generator', 
                'Generate cross-sectional sketches from selected bodies along specified axes.'
            )
        
        # Connect to command created event
        onCommandCreated = CrossSectionCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)
        
        # Execute the command
        cmdDef.execute()
        
        # Keep script running for event handlers
        adsk.autoTerminate(False)
        
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
