# Volatility3GUI


Volatility3GUI is an implemenation of the commandline tool Volatility 3

### Components
  - [Python 3]()
  - [Volatility3](https://github.com/volatilityfoundation/volatility3)
  - [ElectronJS](https://www.electronjs.org/) 
  - [jQuery](https://jquery.com/)
  - [Bootstrap](https://getbootstrap.com/)
  - [Datatables](https://datatables.net/)


### Packaging commands

  - Windows 64-bit Build
      ```bash
      electron-packager . volatility3Gui --platform win32 --arch x64 --prune=true --icon=src/icon.ico --out release-builds/
      ```


  - Linux Build
      ```bash
      electron-packager . volatility3Gui --platform linux --arch x64 --prune=true --out release-builds/
      ```

  
## User Guide

### Requirements
- Volatility3Gui Package
- Python 3

### Launching the Application
  Open Volatility3Gui Package
  Click Volatility3Gui.exe to launch if on Windows
  Run ./Volatilty3Gui in application folder to launch if on Linux

### Updating dependencies
- Click Settings at top right of application
  - Click update Volatility to download the latest version of Volatility 3 from GitHub. - Requires internet access
  - Click update plugins to reload the plugins list if new plugins have been loaded into the folder.

### Selecting a file
To select a file click the Select File or Browse button
- Recommended file types are as follows
  - .dmp .raw .sys .img .bin

### Running a Command
- Once a file has been selected choose from the Platform drop down the operating system the memory sample is from.
- This will give you access to choose the command based on the platform chosen.
- By default only the symbols for Windows are installed but by inserting a symbol table for either Mac or Linux into src\volatility3\volatility\symbols will allow those commands to function.

### Working with the DataTable
  - All successful commands will display their results as a table.
  - To expand the entries viewable select the ‘Show X entries’ dropdown and adjust to desired table size.
  - Datatable can be sorted by clicking on any of the headers displayed
  - To export these results select either Copy, CSV or Excel
  - Exporting will take the entire DataTable, not just what is shown if larger than entry size.

### If Volatility encounters an error running a command
  Pressing ‘ctrl+shift+I’ will open up the console menu and display the arguments passed to the command as well as the error in full received from the command line.
