import PyInstaller.__main__
import os

# Build the cleaner executable
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    '--name=DesktopCleaner',
    '--onefile',
    '--console',  # Keep console for debugging
    '--add-data=config.ini;.',  # Include config.ini
    '--distpath=dist',
    '--workpath=build/cleaner',
    '--specpath=specs',
    os.path.join(current_dir, 'DesktopCleaner.py')
])

print("DesktopCleaner.exe built successfully!")