import PyInstaller.__main__
import os

current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
additional_files = [
    (os.path.join(current_directory, 'requirements', 'hub-base.txt'), '.'),
    (os.path.join(current_directory, 'requirements', 'hub-cpu.txt'), '.'),
    (os.path.join(current_directory, 'requirements', 'hub-builder.txt'), '.'),
]
entry_point = os.path.join(current_directory, "src", "hub.py")

PyInstaller.__main__.run([
    entry_point,
    '--onefile',  # Bundle everything into a single executable
    # '--hidden-import=module_name',  # Uncomment and replace with actual module names if there are hidden imports
    '--clean',  # Clean PyInstaller build folder before building
    '--name=memory-cache-hub-windows',
] + [f'--add-data={src}{os.pathsep}{dst}' for src, dst in additional_files])
