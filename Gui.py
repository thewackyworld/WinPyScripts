from logging import config
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import configparser

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
        browse_btn = tk.Button(file_frame, text="Browse File", 
                              command=self.browse_file,
                              font=("Arial", 12),
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
        
        for text, value in options:
            radio_btn = tk.Radiobutton(options_frame, 
                                      text=text,
                                      variable=self.selected_option,
                                      value=value,
                                      font=("Arial", 10),
                                      anchor="w")
            radio_btn.pack(anchor="w", pady=2)
        
        # Process button
        process_btn = tk.Button(self.root, text="Clean",
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
        
        self.create_task(config)
        # Here i will set the task to run DesktopCleaner.py on the selected schedule

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
        # Here you would implement the logic to create a scheduled task
        # using the selected runtime option and the paths from the config.
        # This is a placeholder for demonstration purposes.
        print(f"Creating task with runtime: {config['RUNTIME']['Choice']} at {config['RUNTIME']['Time']}")
        print("Task created successfully!")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelector(root)
    root.mainloop()
