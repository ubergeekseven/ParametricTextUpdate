import adsk.core
import os
from ...lib import fusionAddInUtils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface


# Command identity information.
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_combineCut'
CMD_NAME = 'Combine Cut'
CMD_Description = 'Cuts sets of objects within a component from anoter body within a chosen component'

# Specify that the command will be promoted to the panel.
IS_PROMOTED = True

# Define the location where the command button will be created.
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidModifyPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []

# Keep track of the number of pairs
pair_count = 1


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get the panel the button will be created in.
    panel = workspace.toolbarPanels.itemById(PANEL_ID)

    # Create the button command control in the UI after the specified existing command.
    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)

    # Specify if the command is promoted to the main toolbar. 
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()


# Function that is called when a user clicks the corresponding button in the UI.
# This defines the contents of the command dialog and connects to the command related events.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    global pair_count
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Created Event')

    # https://help.autodesk.com/view/fusion360/ENU/?contextId=CommandInputs
    inputs = args.command.commandInputs
    group = inputs.addGroupCommandInput('pairs_group', 'Plate/Text Pairs')
    group_inputs = group.children
    # Add the first pair
    add_pair_inputs(group_inputs, 0)
    # Add + button
    inputs.addBoolValueInput('add_pair', 'Add Pair', False, '', False)
    # Add Save and Load buttons
    inputs.addBoolValueInput('save_pairs', 'Save Pairs', False, '', False)
    inputs.addBoolValueInput('load_pairs', 'Load Pairs', False, '', False)
    # Add Info button
    inputs.addBoolValueInput('info', 'Why manual selection?', False, '', False)

    # Connect to the events that are needed by this command.
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.inputChanged, command_input_changed, local_handlers=local_handlers)
    futil.add_handler(args.command.executePreview, command_preview, local_handlers=local_handlers)
    futil.add_handler(args.command.validateInputs, command_validate_input, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)

def add_pair_inputs(group_inputs, idx, target_name=None, tool_name=None):
    """Helper function to add a new pair of inputs"""
    row = group_inputs.addGroupCommandInput(f'row_{idx}', f'Pair {idx+1}')
    row.isExpanded = True
    row_inputs = row.children
    
    # Add plate selection
    plate_input = row_inputs.addSelectionInput(f'plate_{idx}', f'Target Component {idx+1}', 'Select the target component to cut from')
    plate_input.addSelectionFilter('Occurrences')
    plate_input.setSelectionLimits(1, 1)
    if target_name:
        plate_input.tooltip = f'Select the target component named: {target_name}'
        plate_input.prompt = f'Saved: {target_name}'
        # Add read-only text box showing saved name
        row_inputs.addTextBoxCommandInput(f'target_name_{idx}', '', target_name, 1, True)
    
    # Add text selection
    text_input = row_inputs.addSelectionInput(f'text_{idx}', f'Tool Component {idx+1}', 'Select the tool component with bodies to cut from the target component')
    text_input.addSelectionFilter('Occurrences')
    text_input.setSelectionLimits(1, 1)
    if tool_name:
        text_input.tooltip = f'Select the tool component named: {tool_name}'
        text_input.prompt = f'Saved: {tool_name}'
        # Add read-only text box showing saved name
        row_inputs.addTextBoxCommandInput(f'tool_name_{idx}', '', tool_name, 1, True)


# This event handler is called when the user clicks the OK button in the command dialog or 
# is immediately called after the created event not command inputs were created for the dialog.
def command_execute(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Execute Event')
    try:
        # Get the inputs
        inputs = args.command.commandInputs
        group = inputs.itemById('pairs_group')
        if not group:
            futil.log('No pairs group found')
            return
        group_inputs = group.children

        # Get the current design
        app = adsk.core.Application.get()
        design = app.activeProduct
        root_comp = design.rootComponent

        # Process each pair
        for i in range(group_inputs.count):
            item = group_inputs.item(i)
            if item.objectType == adsk.core.GroupCommandInput.classType():
                row_inputs = item.children
                target_input = None
                tool_input = None
                for j in range(row_inputs.count):
                    child = row_inputs.item(j)
                    if child.id.startswith('plate_'):
                        target_input = child
                    elif child.id.startswith('text_'):
                        tool_input = child
                
                if target_input and tool_input and target_input.selectionCount > 0 and tool_input.selectionCount > 0:
                    target_occ = target_input.selection(0).entity
                    tool_occ = tool_input.selection(0).entity
                    
                    # Get the components
                    target_comp = target_occ.component
                    tool_comp = tool_occ.component
                    
                    # Get the target body
                    target_body = target_comp.bRepBodies.itemByName(target_comp.name)
                    if not target_body:
                        ui.messageBox(f'Target body "{target_comp.name}" not found')
                        continue
                    
                    # Create collection of tool bodies
                    tool_bodies = adsk.core.ObjectCollection.create()
                    for body in tool_comp.bRepBodies:
                        tool_bodies.add(body)
                    
                    # Create combine feature
                    combine_features = root_comp.features.combineFeatures
                    combine_input = combine_features.createInput(target_body, tool_bodies)
                    combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
                    combine_input.isKeepToolBodies = True
                    combine_features.add(combine_input)
                    
                    futil.log(f'Created combine feature for {target_comp.name} and {tool_comp.name}')
        
        ui.messageBox('Operation completed successfully.')
    except Exception as e:
        futil.log(f'Error in command execution: {str(e)}')
        ui.messageBox(f'Error: {str(e)}')


# This event handler is called when the command needs to compute a new preview in the graphics window.
def command_preview(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Preview Event')
    inputs = args.command.commandInputs


# This event handler is called when the user changes anything in the command dialog
# allowing you to modify values of other inputs based on that change.
def command_input_changed(args: adsk.core.InputChangedEventArgs):
    import json
    global pair_count
    changed_input = args.input
    inputs = args.inputs
    group = inputs.itemById('pairs_group')
    if not group:
        futil.log('No pairs group found')
        return
    group_inputs = group.children

    futil.log(f'Input changed: {changed_input.id} with value: {changed_input.value}')

    if changed_input.id == 'add_pair':
        pair_count += 1
        idx = pair_count - 1
        add_pair_inputs(group_inputs, idx)
        changed_input.value = False
    elif changed_input.id == 'save_pairs':
        changed_input.value = False
        pairs = []
        # Use itemsByType to get all group inputs in order
        for i in range(group_inputs.count):
            item = group_inputs.item(i)
            if item.objectType == adsk.core.GroupCommandInput.classType():
                row_inputs = item.children
                plate_input = None
                text_input = None
                for j in range(row_inputs.count):
                    child = row_inputs.item(j)
                    if child.id.startswith('plate_'):
                        plate_input = child
                    elif child.id.startswith('text_'):
                        text_input = child
                
                if plate_input and text_input and plate_input.selectionCount > 0 and text_input.selectionCount > 0:
                    target_name = plate_input.selection(0).entity.component.name
                    tool_name = text_input.selection(0).entity.component.name
                    pairs.append({"plate": target_name, "text": tool_name})
        
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plate_text_pairs.json')
        with open(save_path, 'w') as f:
            json.dump(pairs, f)
        ui.messageBox(f'Saved {len(pairs)} pairs.')
    elif changed_input.id == 'load_pairs':
        changed_input.value = False
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plate_text_pairs.json')
        if not os.path.exists(save_path):
            ui.messageBox('No saved pairs found.')
            return
        with open(save_path, 'r') as f:
            pairs = json.load(f)
        # Clear current inputs
        for i in reversed(range(group_inputs.count)):
            group_inputs.item(i).deleteMe()
        # Add loaded pairs with tooltips and default text
        for idx, pair in enumerate(pairs):
            add_pair_inputs(group_inputs, idx, pair["plate"], pair["text"])
        pair_count = len(pairs) if pairs else 1
        if pair_count == 0:  # Ensure at least one pair exists
            add_pair_inputs(group_inputs, 0)
            pair_count = 1
        ui.messageBox(f'Loaded {len(pairs)} pairs. Please reselect the components in the UI.')
    elif changed_input.id == 'info':
        changed_input.value = False
        ui.messageBox('It is annoying, I know. Fusion 360 does not allow add-ins to automatically select components in the UI.\n\nYou must manually reselect the components for each pair. The saved names are shown to help you choose the correct ones.')
    # Update text boxes when a selection changes
    if changed_input.id.startswith('plate_') or changed_input.id.startswith('text_'):
        # Find the index
        if '_' in changed_input.id:
            prefix, idx = changed_input.id.split('_', 1)
            name_box_id = f'{prefix}_name_{idx}'
            name_box = group_inputs.itemById(name_box_id)
            if name_box:
                if changed_input.selectionCount > 0:
                    name_box.text = changed_input.selection(0).entity.component.name
                else:
                    name_box.text = ''
    futil.log(f'{CMD_NAME} Input Changed Event fired from a change to {changed_input.id}')


# This event handler is called when the user interacts with any of the inputs in the dialog
# which allows you to verify that all of the inputs are valid and enables the OK button.
def command_validate_input(args: adsk.core.ValidateInputsEventArgs):
    inputs = args.inputs
    group = inputs.itemById('pairs_group')
    group_inputs = group.children
    
    # Count valid pairs
    valid_pairs = 0
    for i in range(group_inputs.count):
        item = group_inputs.item(i)
        if item.objectType == adsk.core.GroupCommandInput.classType():
            row_inputs = item.children
            plate_input = None
            text_input = None
            for j in range(row_inputs.count):
                child = row_inputs.item(j)
                if child.id.startswith('plate_'):
                    plate_input = child
                elif child.id.startswith('text_'):
                    text_input = child
            
            if plate_input and text_input and plate_input.selectionCount > 0 and text_input.selectionCount > 0:
                valid_pairs += 1
    
    # At least one valid pair is required
    args.areInputsValid = valid_pairs > 0


# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Destroy Event')

    global local_handlers, pair_count
    local_handlers = []
    pair_count = 1 