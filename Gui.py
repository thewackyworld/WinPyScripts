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
        
        # Time selection variables
        self.selected_hour = tk.StringVar()
        self.selected_minute = tk.StringVar()
        self.selected_ampm = tk.StringVar()
        
        # Set default time (current time)
        from datetime import datetime
        now = datetime.now()
        hour_12 = now.hour if now.hour <= 12 else now.hour - 12
        if hour_12 == 0:
            hour_12 = 12
        
        self.selected_hour.set(f"{hour_12:02d}")
        self.selected_minute.set(f"{now.minute:02d}")
        self.selected_ampm.set("AM" if now.hour < 12 else "PM")

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
        
        # TIME SELECTION FRAME
        time_frame = tk.LabelFrame(self.root, text="Schedule Time", 
                                  font=("Arial", 12, "bold"),
                                  padx=15, pady=15)
        time_frame.pack(pady=20, padx=20, fill="x")
        
        time_controls = tk.Frame(time_frame)
        time_controls.pack()
        
        # Hour dropdown
        tk.Label(time_controls, text="Hour:", font=("Arial", 11)).grid(row=0, column=0, padx=5)
        self.hour_combo = ttk.Combobox(time_controls, textvariable=self.selected_hour,
                                      values=[f"{i:02d}" for i in range(1, 13)], 
                                      width=8, state="readonly")
        self.hour_combo.grid(row=0, column=1, padx=5)
        
        # Minute dropdown  
        tk.Label(time_controls, text="Minute:", font=("Arial", 11)).grid(row=0, column=2, padx=5)
        self.minute_combo = ttk.Combobox(time_controls, textvariable=self.selected_minute,
                                        values=[f"{i:02d}" for i in range(0, 60, 5)], 
                                        width=8, state="readonly")
        self.minute_combo.grid(row=0, column=3, padx=5)
        
        # AM/PM dropdown
        tk.Label(time_controls, text="AM/PM:", font=("Arial", 11)).grid(row=0, column=4, padx=5)
        self.ampm_combo = ttk.Combobox(time_controls, textvariable=self.selected_ampm,
                                      values=["AM", "PM"], width=8, state="readonly")
        self.ampm_combo.grid(row=0, column=5, padx=5)
        
        # Display selected time in 24-hour format
        self.time_display_frame = tk.Frame(time_frame)
        self.time_display_frame.pack(pady=(15, 0))
        
        tk.Label(self.time_display_frame, text="Selected Time (24-hour):", 
                font=("Arial", 10)).pack(side="left")
        self.time_display_label = tk.Label(self.time_display_frame, text="00:00", 
                                          font=("Arial", 12, "bold"), 
                                          bg="lightyellow", padx=10, relief="sunken")
        self.time_display_label.pack(side="left", padx=(10, 0))
        
        # Update display when selections change
        self.hour_combo.bind('<<ComboboxSelected>>', self.update_time_display)
        self.minute_combo.bind('<<ComboboxSelected>>', self.update_time_display)
        self.ampm_combo.bind('<<ComboboxSelected>>', self.update_time_display)
        

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
        process_btn = tk.Button(self.root, text="Save Settings",
                               command=self.SetTask,
                               font=("Arial", 14, "bold"),
                               bg="orange", fg="white",
                               width=20, height=2)
        process_btn.pack(padx=20)

        # Delete button
        delete_btn = tk.Button(self.root, text="Delete Old Task",
                               command=self.delete_task,
                               font=("Arial", 10, "bold"),
                               bg="red", fg="white",
                               width=15, height=2)
        delete_btn.pack(pady=5)

        # Initial time display update
        self.update_time_display()

    def get_selected_time_24h(self):
        try:
            hour_12 = int(self.selected_hour.get())
            minute = int(self.selected_minute.get())
            ampm = self.selected_ampm.get()
            
            # Convert to 24-hour format
            if ampm == "AM":
                if hour_12 == 12:
                    hour_24 = 0
                else:
                    hour_24 = hour_12
            else:  # PM
                if hour_12 == 12:
                    hour_24 = 12
                else:
                    hour_24 = hour_12 + 12
            
            return f"{hour_24:02d}:{minute:02d}"
        
        except (ValueError, AttributeError):
            return "00:00"

    def set_time_from_24h(self, time_24h):
        """Convert 24-hour time string back to 12-hour format for GUI"""
        try:
            hour_24, minute = map(int, time_24h.split(':'))
            
            # Convert to 12-hour format
            if hour_24 == 0:
                hour_12 = 12
                ampm = "AM"
            elif hour_24 < 12:
                hour_12 = hour_24
                ampm = "AM"
            elif hour_24 == 12:
                hour_12 = 12
                ampm = "PM"
            else:
                hour_12 = hour_24 - 12
                ampm = "PM"
            
            # Update GUI
            self.selected_hour.set(f"{hour_12:02d}")
            self.selected_minute.set(f"{minute:02d}")
            self.selected_ampm.set(ampm)
            
            # Update display
            self.update_time_display()
            
        except (ValueError, AttributeError):
            pass

    def update_time_display(self, event=None):
        """Convert 12-hour time to 24-hour format and update display"""
        try:
            hour_12 = int(self.selected_hour.get())
            minute = int(self.selected_minute.get())
            ampm = self.selected_ampm.get()
            
            # Convert to 24-hour format
            if ampm == "AM":
                if hour_12 == 12:
                    hour_24 = 0  # 12:XX AM = 00:XX
                else:
                    hour_24 = hour_12  # 1:XX AM = 01:XX, etc.
            else:  # PM
                if hour_12 == 12:
                    hour_24 = 12  # 12:XX PM = 12:XX
                else:
                    hour_24 = hour_12 + 12  # 1:XX PM = 13:XX, etc.
            
            # Format as 24-hour string
            time_24_str = f"{hour_24:02d}:{minute:02d}"
            self.time_display_label.config(text=time_24_str)
            
        except (ValueError, AttributeError):
            self.time_display_label.config(text="--:--")

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
            'Time': self.get_selected_time_24h()
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
    def delete_task(self):
        task_name = "FishsDesktopCleanerTask"
        cmd = ["schtasks", "/delete", "/tn", task_name, "/f"]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            messagebox.showinfo("Task Deleted", f"Task '{task_name}' has been deleted successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to delete task '{task_name}'.\n{e.stderr}")
# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelector(root)
    root.mainloop()
