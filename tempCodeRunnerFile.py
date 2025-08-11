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