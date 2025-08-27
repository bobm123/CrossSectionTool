# Cross-Section Generator for Fusion 360

A Fusion 360 script that automatically generates a series of cross-sectional construction planes from user-selected bodies along specified axes. This tool addresses the common need for creating internal structural frameworks in complex geometries like airplane wings, boat hulls, and other curved or tapered designs.

## Features

- **Multi-body support**: Select multiple solid and surface bodies for cross-section generation
- **Flexible axis selection**: Use any construction axis as the reference for plane distribution
- **Distribution options**: 
  - **Count-based**: Specify number of sections with automatic even spacing
  - **Distance-based**: Specify interval distance (planned feature)
- **Suppression control**: Optional suppression of generated planes for performance
- **Organized output**: All planes are created in the root component with systematic naming
- **Native UI integration**: Uses Fusion 360's standard dialog controls for familiar user experience

## Installation

1. **Download the script**:
   - Clone this repository or download the ZIP file
   - Extract to your desired location

2. **Copy to Fusion 360 Scripts directory**:
   - **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\`
   - **Mac**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/`

3. **File structure after installation**:
   ```
   Scripts/
   └── CrossSectionTool/
       ├── CrossSectionTool.py
       ├── CrossSectionTool.manifest
       └── ScriptIcon.svg
   ```

## Usage

1. **Launch the script**:
   - In Fusion 360, go to **Scripts and Add-ins** > **Scripts**
   - Find and select **Cross-Section Generator**
   - Click **Run**

2. **Configure parameters**:
   - **Bodies**: Select one or more solid or surface bodies
   - **Axis**: Select a construction axis for the section direction
   - **Distribution**: Choose between Count or Distance methods
   - **Suppression**: Check to create planes in suppressed state
   - **Quantity**: Set number of sections (Count mode) or spacing distance

3. **Generate sections**:
   - Click **OK** to create the construction planes
   - Planes will be created in the root component with names like `Section_Plane_001`

## Current Status

This script is in **Phase 1: UI Prototype** stage with basic plane generation functionality:

✅ **Implemented**:
- Complete native API dialog interface
- Parameter collection and validation
- Construction plane generation along selected axes
- Multi-body selection support
- Basic error handling

🚧 **In Development**:
- Distance-based distribution mode
- Cross-section sketch generation from body intersections
- Component-based organization
- Bounding box calculations for automatic spacing

## Technical Details

- **Type**: Fusion 360 Script (single execution)
- **API**: Fusion 360 Python API
- **Language**: Python 3.x
- **UI Framework**: Native Fusion 360 CommandInput controls

### Key Components

- **Dialog System**: Uses SelectionCommandInput, DropDownCommandInput, and BoolValueInput
- **Plane Creation**: Utilizes `setByDistanceOnPath` with normalized distances (0-1 range)
- **Event Handling**: Implements proper command lifecycle with creation, execution, and destruction handlers
- **Error Recovery**: Multiple fallback methods for plane creation

## Requirements

- Autodesk Fusion 360 (any recent version with Python API support)
- At least one solid or surface body in the active design
- A construction axis for section reference

## Target Users

- **Hobbyist makers** building RC aircraft, boats, and mechanical projects
- **Engineering students** working on design projects requiring structural analysis
- **Prototyping engineers** in aerospace, marine, and automotive industries

## Future Enhancements

- **Sketch Generation**: Automatic creation of cross-section sketches from body intersections
- **Parametric Relationships**: Editable offset planes with sketch regeneration
- **Advanced Distribution**: Custom spacing patterns and distance-based modes
- **Export Options**: DXF export and technical drawing generation
- **Real-time Preview**: Visual feedback during plane positioning

## Contributing

This project follows the product requirements outlined in `DesignDocs/CrossSectionTool-PRD.md`. Contributions should align with the documented architecture and user experience goals.

## Support

For issues and feature requests, please refer to the project's issue tracker. The tool is designed to integrate seamlessly with Fusion 360's native workflow and follows Autodesk's development guidelines.

## License

Developed for educational and professional use in Fusion 360 environments.