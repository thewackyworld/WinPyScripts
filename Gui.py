from logging import config
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import configparser
import subprocess
import sys

class FileSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Cleaner")
        self.root.geometry("600x700")
        
        # Variable to store selected file path
        self.selected_file = tk.StringVar()
        self.selected_file.set("No file selected")
        
        # Variable for radio button selection
        self.selected_option = tk.StringVar()
        self.selected_option.set("option1")  # Default selection
        
        self.selected_time = tk.StringVar()
        self.selected_time.set("00:00")  # Default time

        self.create_widgets()
    
    def create_widgets(self):
        # Big title at the top
        title_label = tk.Label(self.root, text="Desktop Cleaner", 
                              font=("Arial", 24, "bold"), 
                              fg="Gold", pady=20)
        title_label.pack()
        
        # File selection frame
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=20, padx=20, fill="x")
        
        # Browse button
        browse_btn = tk.Button(file_frame, text="Select destination", 
                              command=self.browse_file,
                              font=("Arial", 10),
                              bg="lightgreen", width=15)
        browse_btn.pack(side="left", padx=(0, 10))
        
        # Selected file path display
        path_label = tk.Label(file_frame, textvariable=self.selected_file,
                             font=("Arial", 10),
                             bg="white", relief="sunken",
                             anchor="w", padx=10)
        path_label.pack(side="left", fill="x", expand=True)
        
        # Separator
        separator = ttk.Separator(self.root, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=20)
        
        # Options frame at bottom
        options_frame = tk.LabelFrame(self.root, text="RunTime Options", 
                                     font=("Arial", 12, "bold"),
                                     padx=10, pady=10)
        options_frame.pack(pady=20, padx=20, fill="x")
        
        # Radio buttons (only one can be selected)
        options = [
            ("Daily", "option1"),
            ("Weekly", "option2"),
            ("Monthly", "option3"),
            ("onStart", "option4"),
            ("once", "option5")
        ]
        
        # Add this to your existing GUI
        time_frame = tk.LabelFrame(self.root, text="Schedule Time")
        time_frame.pack(pady=20)

        # Hour dropdown
        hour_combo = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(1, 13)])
        hour_combo.pack(side="left", padx=5)

        # AM/PM
        ampm_combo = ttk.Combobox(time_frame, values=["AM", "PM"])
        ampm_combo.pack(side="left", padx=5)

        for text, value in options:
            radio_btn = tk.Radiobutton(options_frame, 
                                      text=text,
                                      variable=self.selected_option,
                                      value=value,
                                      font=("Arial", 10),
                                      anchor="w")
            radio_btn.pack(anchor="w", pady=2)
        
        # Process button
        process_btn = tk.Button(self.root, text="Save Settings",
                               command=self.SetTask,
                               font=("Arial", 14, "bold"),
                               bg="orange", fg="white",
                               width=20, height=2)
        process_btn.pack(pady=20)
    
    def browse_file(self):
        file_path = filedialog.askdirectory(
            title="Select a folder",
        )
        
        if file_path:
            self.selected_file.set(file_path)
    
    def SetTask(self):
        if self.selected_file.get() == "No file selected":
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        
        # Get the selected option text
        option_map = {
            "option1": "daily",
            "option2": "weekly",
            "option3": "monthly",
            "option4": "onStart",
            "option5": "once"
        }

        selected_text = option_map[self.selected_option.get()]
        self.selected_option.set(selected_text)

        print(self.selected_file.get())

        messagebox.showinfo("Setting Cleaners Schedule", 
                           f"Destination File: {self.selected_file.get()}\n"
                           f"Runtime: {selected_text}\n\n"
                           f"Loading ConfigFile...")
        config = self.load_config()
        
        messagebox.showinfo("Config Loaded", 
                           "Creating Shelfs.....")
        
        self.create_folders(config)
        
        messagebox.showinfo("Shelves Created", 
                           "Setting task.....")
        
        if self.create_task(config):
            messagebox.showinfo("Task Created", 
                               f"Desktop Cleaner is set to run on {selected_text} schedule.")
        else:
            messagebox.showerror("Error", "Failed to create the task. Please check the console for details.")

    def load_config(self ,filename = "config.ini"):
        config = configparser.ConfigParser()

        self.create_default_ini(filename)

        config.read(filename)

        config['PATHS']['destination'] = os.path.join(self.selected_file.get(), "DesktopArchive")

        config = self.SetConfig(config)

        with open(filename, 'w') as configfile:
            config.write(configfile)
        return config

    def SetConfig(self, config):
        config['DPATHS'] = {
            'shortcut_path': os.path.join(config['PATHS']['destination'], 'Shortcuts'),
            'folders_path': os.path.join(config['PATHS']['destination'], 'Folders'),
            'game_path': os.path.join(config['PATHS']['destination'], 'Games_Shortcuts'),
            'pdf_path': os.path.join(config['PATHS']['destination'], 'Pdfs'),
            'zip_path': os.path.join(config['PATHS']['destination'], 'Zip_files'),
            'others_path': os.path.join(config['PATHS']['destination'], 'Others'),
            'image_path': os.path.join(config['PATHS']['destination'], 'Images')
        }
        config['RUNTIME'] = {
            'Choice': self.selected_option.get(),
            'Time': '00:00'  # Default time, can be changed later
        }
        return config
    
    def create_default_ini(self, filename):
        config = configparser.ConfigParser()
        config['PATHS'] = {
            'desktop': os.path.join(os.path.expanduser("~"), "Desktop"),
            'destination': "DesktopArchive"
        }
        config['DPATHS'] = {

        }
        config['RUNTIME'] = {
            'Choice': 'daily',
            'Time': '00:00'
        }
        config['EXCEPTIONS'] = {
            'Name': 'Desktop.ini, Codes'
        }
        
        with open(filename, 'w') as configfile:
            config.write(configfile)

    def create_folders(self, config):
        for key, path in config['DPATHS'].items():
            os.makedirs(path, exist_ok=True)

    def create_task(self, config):
        script_path = os.path.abspath("DesktopCleaner.py")
        python_path = sys.executable
        task_name = "FishsDesktopCleanerTask"
        schedule_time = config['RUNTIME']['Time']
        cmd = [
            "schtasks",
            "/create",
            "/tn", task_name, # Task name
            "/tr", f'"{python_path}" "{script_path}"',  # Task to run
            "/sc", "daily",  # Schedule type
            "/st", schedule_time,  # Start time
            "/f"  # Force create (overwrites if exists)
        ]
        try:
            # Run the command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"Task '{task_name}' created successfully!")
            print(f"Will run daily at {schedule_time}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating task: {e}")
            print(f"Error output: {e.stderr}")
            return False
        
# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelector(root)
    root.mainloop()
