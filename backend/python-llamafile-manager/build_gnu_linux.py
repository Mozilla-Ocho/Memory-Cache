import PyInstaller.__main__
import os

# Define the path to the directory containing the llamafiles and other necessary files.
# Assuming these files are in the same directory as the script for simplicity.
current_directory = os.path.dirname(os.path.abspath(__file__))

# List of tuples specifying additional files/directories and their destination in the distribution.
# Adjust paths as necessary.
additional_files = [
    (os.path.join(current_directory, 'requirements.txt'), '.'),
    # Add other necessary files or directories here.
    # Example: (os.path.join(current_directory, 'data_folder'), 'data_folder')
]

# Entry point of the application
entry_point = os.path.join(current_directory, 'manager.py')

# Build the application with PyInstaller
PyInstaller.__main__.run([
    entry_point,
    '--onefile',  # Bundle everything into a single executable
    '--add-data=' + ';'.join([f'{src}{os.pathsep}{dst}' for src, dst in additional_files]),  # Add additional files/directories
    # '--hidden-import=module_name',  # Uncomment and replace with actual module names if there are hidden imports
    '--clean',  # Clean PyInstaller build folder before building
    '--name=python-llamafile-manager-gnu-linux',  # Name of the generated executable
    # Additional flags can be added as needed.
])
