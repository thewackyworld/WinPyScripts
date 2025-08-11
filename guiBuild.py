import PyInstaller.__main__
import os

# Build the GUI executable
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    '--name=AquariumDesktop',
    '--onefile',
    '--windowed',  # No console for GUI
    '--add-data=DesktopCleaner.exe;.',  # Include the cleaner executable
    '--distpath=dist',
    '--workpath=build/gui',
    '--specpath=specs',
    os.path.join(current_dir, 'Gui.py')
])

print("Aquarium cleaner.exe built successfully!")