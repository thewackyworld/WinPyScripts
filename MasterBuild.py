import PyInstaller.__main__
import os
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))

print("Building DesktopCleaner.exe...")
# Build cleaner first
PyInstaller.__main__.run([
    '--name=DesktopCleaner',
    '--onefile',
    '--console',
    '--distpath=dist',
    '--workpath=build/cleaner',
    '--specpath=specs',
    os.path.join(current_dir, 'DesktopCleaner.py')
])

print("Building GUI with embedded cleaner...")
# Build GUI with cleaner embedded
PyInstaller.__main__.run([
    '--name=AquariumDesktop',
    '--onefile',
    '--windowed',
    '--add-data=dist/DesktopCleaner.exe;.',  # Include the built cleaner
    '--distpath=dist',
    '--workpath=build/gui',
    '--specpath=specs',
    os.path.join(current_dir, 'Gui.py')
])

print("Build complete!")
print("Distribute: dist/AquariumDesktop.exe")
print("This contains everything needed - no Python installation required!")