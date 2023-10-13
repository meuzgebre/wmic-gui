# WMIC-GUI: Windows System Information Viewer

WMIC-GUI is a Python application that allows you to retrieve and display system information from a Windows machine using the Windows Management Instrumentation Command-line (WMIC). This GUI application provides an easy-to-use interface to view various system attributes and their values.

## Features

- View system information in a user-friendly tabbed interface.
- Retrieve information about the operating system, CPU, disk drives, logical disks, memory chips, baseboard, and BIOS.
- Customizable design with modern UI elements.

## Prerequisites

Before running WMIC-GUI, ensure that you have the following prerequisites installed on your system:

- Python 3.x
- Tkinter: Python's standard GUI library
- WMIC: Windows Management Instrumentation Command-line

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/wmic-gui.git
cd wmic-gui
python wmic_gui.py
```

## Usage

- Launch the application, and you will see a tabbed interface with categories like "OS," "CPU," "DiskDrive," and more.
- Click on a tab to view information about the selected category.
- Enjoy exploring the system attributes and their values in a clean and organized format.

## Known Issues

- Please note that this application is designed for Windows systems only, as it relies on WMIC commands.
