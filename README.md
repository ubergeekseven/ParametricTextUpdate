# CombineCut Fusion 360 Add-in

A Fusion 360 add-in that allows choosing components and tools for cutting operations.

## Features
- Choose components and tools for cutting operations
- Support for parametric text and objects
- Compatible with both Windows and Mac

## Installation Instructions

### Automated Installation (Recommended)

#### Windows Users
1. Download the latest release from the [Releases](https://github.com/yourusername/CombineCut/releases) page
2. Extract the ZIP file
3. Double-click `install.bat`
4. Follow the on-screen instructions
   - If Python is not installed, the installer will guide you through the installation process
5. Restart Fusion 360 if it's running
6. The add-in should appear in the Add-Ins dialog (Press Shift+S to open)
7. Enable the add-in by checking its checkbox

#### Mac Users
1. Download the latest release from the [Releases](https://github.com/yourusername/CombineCut/releases) page
2. Extract the ZIP file
3. Open Terminal and navigate to the extracted folder
4. Run: `python3 install.py`
5. Follow the on-screen instructions
6. Restart Fusion 360 if it's running
7. The add-in should appear in the Add-Ins dialog (Press Shift+S to open)
8. Enable the add-in by checking its checkbox

### Manual Installation (Alternative)
If the automated installation doesn't work, you can install manually:

#### Windows
1. Download the latest release from the [Releases](https://github.com/yourusername/CombineCut/releases) page
2. Extract the ZIP file
3. Copy the entire `CombineCut` folder to:
   ```
   %APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\
   ```
   (You can paste this path in Windows Explorer's address bar)
   - The final path should look like: `C:\Users\YourUsername\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\CombineCut`

#### Mac
1. Download the latest release from the [Releases](https://github.com/yourusername/CombineCut/releases) page
2. Extract the ZIP file
3. Copy the entire `CombineCut` folder to:
   ```
   ~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/
   ```
   - The final path should look like: `/Users/YourUsername/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/CombineCut`

### Troubleshooting
If the add-in doesn't appear:
1. Verify the folder structure is correct:
   ```
   CombineCut/
   ├── CombineCut.manifest
   ├── CombineCut.py
   ├── AddInIcon.svg
   ├── commands/
   ├── lib/
   └── README.md
   ```
2. Check that all files were copied correctly
3. Ensure you have the correct permissions to access the AddIns folder
4. Try restarting Fusion 360
5. If using the automated installer:
   - Windows: Check if Python is installed and in your PATH
   - Mac: Make sure you're using Python 3.6 or later
   - Check the console output for any error messages

## Usage
[Add your usage instructions here]

## Requirements
- Fusion 360 (version 2.0.0 or later)
- Windows 10/11 or macOS
- Python 3.6 or later (for automated installation)
  - Windows users: The installer will guide you through Python installation if needed

## Version History
- 1.0.0 (Current)
  - Initial release
  - Basic combine/cut functionality
  - Support for parametric text and objects
  - Automated installation support with batch installer for Windows

## Support
[Add your support information here]

## License
[Add your license information here] 