import PyInstaller.__main__
import os

current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Print the files in the current directory for debugging purposes
print(f'Files in {current_directory}:')
for file in os.listdir(current_directory):
    print(file)

# List of tuples specifying additional files/directories and their destination in the distribution.
# Adjust paths as necessary.
additional_files = [
    #(os.path.join(current_directory, 'requirements.txt'), '.'),
    (os.path.join(current_directory, 'requirements', 'hub-base.txt'), '.'),
    (os.path.join(current_directory, 'requirements', 'hub-cpu.txt'), '.'),
    (os.path.join(current_directory, 'requirements', 'hub-builder.txt'), '.'),

    # Add other necessary files or directories here.
    # Example: (os.path.join(current_directory, 'data_folder'), 'data_folder')
]

# Entry point of the application
entry_point = os.path.join(current_directory, "src", "hub.py")


# Add an `--add-data` flag for each additional file/directory
# `--add-data` flag format: `--add-data 'source_path:destination_path'`

# Build the application with PyInstaller
PyInstaller.__main__.run([
    entry_point,
    '--onefile',  # Bundle everything into a single executable
    # '--hidden-import=module_name',  # Uncomment and replace with actual module names if there are hidden imports
    '--clean',  # Clean PyInstaller build folder before building
    '--name=memory-cache-hub-macos',  # Name of the generated executable
    # Additional flags can be added as needed.
] + [f'--add-data={src}{os.pathsep}{dst}' for src, dst in additional_files])
