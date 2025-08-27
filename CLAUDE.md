# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Fusion 360 script for automatically generating cross-sectional sketches from selected bodies along specified axes. The tool is designed to help users create internal structural frameworks for complex geometries like airplane wings and boat hulls.

## Architecture

**Script Type**: Fusion 360 Script (not Add-in)
- Single-execution model that runs, completes task, and terminates
- Uses Fusion 360 Python API 
- Accessed via Scripts and Add-ins > Scripts menu
- No persistent UI or background processes

**Core Components**:
- `CrossSectionTool.py` - Main script with basic Fusion 360 boilerplate
- `CrossSectionTool.manifest` - Script metadata and configuration
- `DesignDocs/CrossSectionTool-PRD.md` - Comprehensive product requirements document

## Key Technical Requirements

**Parametric Architecture**: 
- Create offset planes as parametric features with editable distance parameters
- Attach cross-section sketches to offset planes
- Maintain parent-child relationships between bodies, planes, and sketches
- Enable sketch regeneration when plane parameters change

**Multi-Body Processing**:
- Support selection of multiple solid and surface bodies
- Use BRep intersection capabilities for geometry processing
- Create consolidated sketches when multiple bodies intersect at same plane
- Calculate bounding boxes across all selected bodies

**UI Design**:
- Custom dialog using native Fusion 360 UI controls
- Axis selector (X/Y/Z axes only)
- Body selection with visual count indicators
- Distribution options: Count-based or Distance-based spacing
- Progress indicators for batch operations
- Contextual help tooltips for all controls

## Current Status

The project currently contains only basic boilerplate code. The main implementation needs to be built according to the specifications in the PRD.

## Development Workflow

**Testing**: 
- Deploy to Fusion 360 Scripts directory: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\CrossSectionTool\`
- Test directly in Fusion 360 via Scripts menu
- No external testing framework currently configured

**File Organization**:
- All generated elements should be organized in dedicated components
- Use naming convention: "Body1_Section_001", "Body2_Section_001", etc.
- Maintain timeline integration for easy modification history

**Performance Targets**:
- 5 cross-sections on simple geometry: <5 seconds
- 20 cross-sections on complex geometry: <30 seconds
- Efficient memory management for large models