from distutils.core import setup
import py2exe
import sys

# Remove the console option
sys.argv.append("py2exe")

# Define the GUI application
setup(
    options={
        "py2exe": {
            "bundle_files": 1,  # Create a single executable file
            "compressed": True,  # Compress the library archive
            "dll_excludes": ['w9xpopen.exe']  # Exclude unnecessary DLLs
        }
    },
    windows=[{"script": "main.py", "dest_base": "wmic gui"}]
)
