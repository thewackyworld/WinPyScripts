import configparser
import os
import shutil
import sys

def move_with_rename(src, dst_folder):
    filename = os.path.basename(src)
    name, ext = os.path.splitext(filename)
    dst = os.path.join(dst_folder, filename)
    counter = 1
    while os.path.exists(dst):
        dst = os.path.join(dst_folder, f"{name}_{counter}{ext}")
        counter += 1
    shutil.move(src, dst)

def load_config(filename="config.ini"):
    config = configparser.ConfigParser()
    
    # Look for config in these locations (in order of preference)
    config_paths = [
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "AquariumCleaner", filename),  # Permanent location
        filename,  # Current directory
        os.path.join(os.path.dirname(sys.executable), filename),  # Same dir as exe
    ]
    
    config_found = False
    for config_path in config_paths:
        if os.path.exists(config_path):
            print(f"Found config at: {config_path}")
            config.read(config_path)
            config_found = True
            break
    
    if not config_found:
        print(f"ERROR: No config.ini found in any of these locations:")
        for path in config_paths:
            print(f"  - {path}")
        raise FileNotFoundError("config.ini not found. Please run the GUI first to create configuration.")
    
    return config

try:
    print("Desktop Cleaner starting...")
    config = load_config()
    
    desktop_path = config['PATHS']['desktop']
    destination_path = config['PATHS']['destination'] 
    shortcut_path = config['DPATHS']['shortcut_path']
    folders_path = config['DPATHS']['folders_path']
    game_path = config['DPATHS']['game_path']
    pdf_path = config['DPATHS']['pdf_path']
    zip_path = config['DPATHS']['zip_path']
    others_path = config['DPATHS']['others_path']
    image_path = config['DPATHS']['image_path']
    exceptions = config['EXCEPTIONS']['Name'].split(', ')

    print(f"Desktop path: {desktop_path}")
    print(f"Destination: {destination_path}")

    # Create directories if they don't exist
    for path in [shortcut_path, folders_path, game_path, pdf_path, zip_path, others_path, image_path]:
        os.makedirs(path, exist_ok=True)

    # Process files
    files_moved = 0
    for filename in os.listdir(desktop_path):
        file_path = os.path.join(desktop_path, filename)
        
        # Skip certain system folders if needed
        if filename in exceptions:
            print(f"Skipping: {filename}")
            continue
            
        if os.path.isfile(file_path):
            if filename.endswith(".lnk"):
                move_with_rename(file_path, shortcut_path)
                print(f"Moved shortcut: {filename}")
            elif filename.endswith(".url"):
                move_with_rename(file_path, game_path)
                print(f"Moved URL: {filename}")
            elif filename.endswith(".pdf"):
                move_with_rename(file_path, pdf_path)
                print(f"Moved PDF: {filename}")
            elif filename.endswith((".zip", ".rar", ".7z")):
                move_with_rename(file_path, zip_path)
                print(f"Moved archive: {filename}")
            elif filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
                move_with_rename(file_path, image_path)
                print(f"Moved image: {filename}")
            else:
                move_with_rename(file_path, others_path)
                print(f"Moved other file: {filename}")
            files_moved += 1
        elif os.path.isdir(file_path):
            # Handle folders - move them to a separate folders directory
            move_with_rename(file_path, folders_path)
            print(f"Moved folder: {filename}")
            files_moved += 1

    print(f"Desktop cleaning completed! Moved {files_moved} items.")

except Exception as e:
    print(f"Error during desktop cleaning: {e}")
    import traceback
    traceback.print_exc()
    # Keep console open to see the error
    input("Press Enter to exit...")
