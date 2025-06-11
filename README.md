# KSP Mod Manager

A powerful and user-friendly mod profile manager for Kerbal Space Program that allows you to easily switch between different mod configurations without the hassle of manually copying files.

## Features

### 🚀 **Multi-Instance Support**
- Manage multiple KSP installations simultaneously
- Automatic KSP installation validation with comprehensive checks
- Support for different KSP versions and installations
- Smart executable detection (KSP.exe, KSP_x64.exe, etc.)

### 📋 **Enhanced Profile Management**
- Create unlimited mod profiles for different gameplay styles
- **NEW**: Choose between blank profiles or select from cached mods when creating
- **NEW**: Advanced mod selection dialog with search and filtering
- **NEW**: Manage existing profile mods with intuitive interface
- Apply profiles with a single click
- Update profiles from your current GameData setup
- Visual mod list display for each profile

### 🔧 **Smart Mod Handling**
- Automatic mod discovery and organization
- Safe file operations with comprehensive error handling
- Preserve stock KSP files (Squad, SquadExpansion folders)
- Natural sorting for better mod organization
- **NEW**: Clean up unused mods functionality

### 🛡️ **Backup & Safety**
- Create zip backups of your GameData folder
- Rollback protection with atomic operations
- Clean removal of unused mods
- Comprehensive validation before operations
- Enhanced error handling and recovery

### 🎯 **Quality of Life**
- **NEW**: Color-coded UI with intuitive button styling
- **NEW**: Enhanced tooltips for better user guidance
- **NEW**: Improved mod selection dialog with persistent selections
- **NEW**: Search and filter functionality in mod selection
- Status updates during operations
- Cross-platform compatibility (Windows focus)
- Elevated privileges handling for protected installations

## Installation

### Requirements
- Python 3.7 or higher
- Windows (primary support), Linux/Mac (community tested)
- Kerbal Space Program installation

### Quick Start
1. Download the latest release from the [Releases](../../releases) page
2. Extract to your desired location
3. Run `main.py` with Python
4. Add your KSP installation by clicking the "+" button next to the instance dropdown
5. Start creating profiles!

### From Source
```bash
git clone https://github.com/Lack-Of-Name/KSP-Mod-Profile-Manager
cd KSP-Mod-Profile-Manager
python main.py #-d switch if errors
```

## Usage

### Setting Up Your First Instance
1. Click the **"+"** button (light green) next to the instance dropdown
2. Select your KSP executable (KSP.exe, KSP_x64.exe, etc.)
3. The tool will automatically validate your installation and detect GameData
4. Give your instance a memorable name

### Creating Profiles
1. Select your KSP instance
2. Click the **"+"** button (light green) next to the profile dropdown
3. Choose your creation method:
   - **Create Blank Profile**: Start with an empty profile
   - **Choose from Cached Mods**: Select from available mods in your mods folder
4. Name your profile and configure as needed

### Managing Profile Mods
- **Manage Profile Mods** (salmon button): Add or remove mods from the selected profile
- Use the search functionality to quickly find mods
- Select/deselect multiple mods with "Select All" and "Select None" buttons
- Real-time filtering maintains your selections

### Core Operations
- **Apply Selected Profile** (royal blue): Replaces your GameData with the selected profile's mods
- **Update Profile from GameData** (violet): Updates the selected profile with your current GameData contents
- **Backup GameData** (default): Creates a timestamped zip backup
- **Clean Up Unused Mods** (default): Removes mods not referenced in any profile

## New Features in This Version

### 🎨 **Enhanced User Interface**
- Color-coded buttons for better visual organization
- Improved button styling and layout
- Enhanced tooltips with detailed descriptions

### 🔍 **Advanced Mod Selection**
- Interactive mod selection dialog with search functionality
- Persistent selections that maintain state during filtering
- Real-time mod counting and selection feedback
- Support for large mod collections

### 🛠️ **Improved Profile Management**
- Two methods for profile creation (blank or from cached mods)
- Direct profile mod management without recreating profiles
- Better handling of profile updates and modifications

### 🧹 **Cleanup Tools**
- Automatic detection of unused mods across all profiles
- Safe removal with user confirmation
- Detailed feedback during cleanup operations

## Directory Structure

```
ksp-mod-manager/
├── main.py              # Main application
├── instances.json       # KSP instance configurations
├── mods/               # Cached mod files
│   ├── ModName1/
│   └── ModName2/
├── profiles/           # Profile definitions by instance
│   └── InstanceName/
│       ├── Profile1.json
│       └── Profile2.json
└── backups/           # GameData backups
    └── Instance-Profile-timestamp.zip
```

## Safety Features

- **Enhanced Validation**: Comprehensive KSP installation validation
- **Automatic Backups**: Always backup before major operations
- **Stock File Protection**: Never modifies core KSP files (Squad, SquadExpansion)
- **Atomic Operations**: All-or-nothing profile applications
- **Error Recovery**: Comprehensive error handling and reporting
- **Permission Handling**: Automatic elevation for protected directories

## Debug Mode

Run with debug flag for detailed error information:
```bash
python main.py -d
```

## Security Notice

This application requires elevated privileges on Windows to manage files in protected directories (like Program Files). 

**VirusTotal Scan**: 
(https://www.virustotal.com/gui/file/2528a323ba6f860df870a91dda96e5eef6818855e01a96bad58a8b61ae58d563?nocache=1)

The application will automatically request administrator rights when needed. This is normal and required for proper operation with KSP installations in system directories.

## UI Color Guide

- **Light Green (+)**: Add new instances or profiles
- **Red (−)**: Remove/delete operations
- **Royal Blue**: Primary actions (Apply Profile)
- **Violet**: Update operations
- **Light Salmon**: Management operations
- **Default Gray**: Utility operations (Backup, Cleanup)

## Compatibility

### Supported KSP Versions
- KSP 1.x series (all versions)
- Works with modded and stock installations
- Compatible with CKAN-managed installations

### Operating Systems
- **Windows**: Full support with elevated privileges
- **Linux**: Community supported
- **macOS**: Community supported

## Contributing

Contributions are welcome! Here's how you can help:

### 🐛 **Bug Reports**
- Use the [Issues](../../issues) page
- Include your OS, Python version, and KSP version
- Provide steps to reproduce the issue
- Include error messages and logs

### 💡 **Feature Requests**
- Check existing [Issues](../../issues) first
- Describe your use case and proposed solution
- Consider implementation complexity

### 🔧 **Code Contributions**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### 📝 **Documentation**
- Improve README documentation
- Add code comments
- Create usage guides
- Update help text and tooltips

## Development Guidelines

- Follow existing code style and patterns
- Add error handling for new operations
- Test with multiple KSP versions when possible
- Consider cross-platform compatibility
- Update tooltips and help text for new features
- Maintain color consistency in UI elements

## Roadmap

- [ ] Mod dependency management
- [ ] Profile sharing and templates
- [ ] Enhanced mod conflict detection
- [ ] Configuration file management
- [ ] Automated mod updates
- [ ] Drag-and-drop mod organization
- [ ] Profile comparison tools

## FAQ

**Q: Will this work with CKAN?**
A: Yes! The tool works alongside CKAN installations. However, be careful not to conflict with CKAN's mod management.

**Q: Can I use this with multiple KSP versions?**
A: Absolutely! That's exactly what the multi-instance support is for.

**Q: What happens to my save files?**
A: Save files are never touched. This tool only manages the GameData folder.

**Q: Is it safe?**
A: Yes, the tool includes multiple safety features including automatic backups and validation checks.

**Q: How do I search for mods when creating profiles?**
A: Use the search box in the mod selection dialog - it filters mods in real-time while preserving your selections.

**Q: Can I modify an existing profile?**
A: Yes! Use the "Manage Profile Mods" button to add or remove mods from any existing profile.

## License

This project is licensed under the MIT License

## Acknowledgments

- The KSP modding community for inspiration
- Contributors and testers
- Squad/Private Division for Kerbal Space Program
- https://Claude.ai

## Support

- **Issues**: Use the GitHub [Issues](../../issues) page
- **Discussions**: Check [Discussions](../../discussions) for questions
- **KSP Forums**: [Link to KSP forum thread - if applicable]

---

**Disclaimer**: This tool is not affiliated with Squad or Private Division. Kerbal Space Program is a trademark of Private Division. Always backup your saves and installations before using any mod management tools.
