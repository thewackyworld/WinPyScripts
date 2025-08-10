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

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop") # finds the desktop of the pc

# should be read from the config file
destination_path = "" #os.path.join("D:\\DesktopArchive")

# this will happen on the gui only first time it is run
# shortcut_path = os.path.join(destination_path, "Shortcuts")
# folders_path = os.path.join(destination_path, "Folders")
# game_path = os.path.join(destination_path, "Games_Shortcuts")
# pdf_path = os.path.join(destination_path, "Pdfs")
# zip_path = os.path.join(destination_path, "Zip_files")
# others_path = os.path.join(destination_path, "Others")
# image_path = os.path.join(destination_path, "Images")

# move it to gui code
# os.makedirs(shortcut_path, exist_ok=True)
# os.makedirs(destination_path, exist_ok=True)
# os.makedirs(folders_path, exist_ok=True)
# os.makedirs(game_path, exist_ok=True)
# os.makedirs(pdf_path, exist_ok=True)
# os.makedirs(zip_path, exist_ok=True)
# os.makedirs(others_path, exist_ok=True)
# os.makedirs(image_path, exist_ok=True)

for filename in os.listdir(desktop_path):
    file_path = os.path.join(desktop_path, filename)
    
    # Skip certain system folders if needed
    if filename in ["Desktop.ini", "Codes"]:
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
