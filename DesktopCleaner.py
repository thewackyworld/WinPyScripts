import configparser
import os
import shutil

def move_with_rename(src, dst_folder):
    filename = os.path.basename(src)
    name, ext = os.path.splitext(filename)
    dst = os.path.join(dst_folder, filename)
    counter = 1
    while os.path.exists(dst):
        dst = os.path.join(dst_folder, f"{name}_{counter}{ext}")
        counter += 1
    shutil.move(src, dst)

def load_config(filename = "config.ini"):
        config = configparser.ConfigParser()
        config.read(filename)
        return config

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

for filename in os.listdir(desktop_path):
    file_path = os.path.join(desktop_path, filename)
    
    # Skip certain system folders if needed
    if filename in exceptions:
        continue
        
    if os.path.isfile(file_path):
        if filename.endswith(".lnk"):
            move_with_rename(file_path, shortcut_path)
        elif filename.endswith(".url"):
            move_with_rename(file_path, game_path)
        elif filename.endswith(".pdf"):
            move_with_rename(file_path, pdf_path)
        elif filename.endswith((".zip", ".rar", ".7z")):
            move_with_rename(file_path, zip_path)
        elif filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            move_with_rename(file_path, image_path)
        else:
            move_with_rename(file_path, others_path)
    elif os.path.isdir(file_path):
        # Handle folders - move them to a separate folders directory
        move_with_rename(file_path, folders_path)
