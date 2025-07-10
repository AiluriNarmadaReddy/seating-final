"""
Main Window View - Main application window
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from utils.constants import APP_TITLE, INSTITUTION_NAME


class MainWindow:
    """
    MainWindow class representing the main application window
    """
    def __init__(self, controller):
        """
        Initialize the main window
        
        Args:
            controller: Main controller instance
        """
        self.controller = controller
        self.root = tk.Tk()
        
        # Configure main window
        self.root.title(APP_TITLE)
        self.root.protocol("WM_DELETE_WINDOW", self.controller.exit_application)
        
        # Get screen dimensions for full-screen window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # Setup UI components
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface components"""
        # Try to load background image
        try:
            bg_image_path = os.path.join('resources', 'background.jpg')
            if os.path.exists(bg_image_path):
                bg_image = Image.open(bg_image_path)
                bg_image = bg_image.resize(
                    (self.root.winfo_screenwidth(), self.root.winfo_screenheight()), 
                    Image.LANCZOS
                )
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                bg_label = tk.Label(self.root, image=self.bg_photo)
                bg_label.place(relwidth=1, relheight=1)
            else:
                # If image file doesn't exist, use plain background
                self.root.configure(bg='#E6E6FA')
        except Exception:
            # If image loading fails, use plain background
            self.root.configure(bg='#E6E6FA')
        
        # Add institution name header
        header_label = tk.Label(
            self.root,
            text=INSTITUTION_NAME,
            fg='#87CEEB',
            font=("Comic Sans MS", 30, 'bold', 'italic', "underline"),
            bg='#E6E6FA' if not hasattr(self, 'bg_photo') else None
        )
        header_label.place(x=130, y=5)
        
        # Add application title
        title_label = tk.Label(
            self.root,
            text="Seating Arrangement For External Examinations",
            fg='#87CEEB',
            font=("Comic Sans MS", 25, 'bold', 'italic', "underline"),
            bg='#E6E6FA' if not hasattr(self, 'bg_photo') else None
        )
        title_label.place(x=300, y=80)
        
        # Add buttons
        self._create_buttons()
    
    def _create_buttons(self):
        """Create main navigation buttons"""
        # Rooms management button
        halls_btn = tk.Button(
            self.root,
            text='Halls',
            bg='#87CEEB',
            fg='#FFFFFF',
            font=("Comic Sans MS", 30, 'bold', 'italic'),
            command=self.controller.open_rooms
        )
        halls_btn.place(x=350, y=280)
        
        # Hall plan and summary button
        hall_plan_btn = tk.Button(
            self.root,
            text='Hall Plan &\nSummary Sheet',
            bg='#87CEEB',
            fg='#FFFFFF',
            font=("Comic Sans MS", 20, 'bold', 'italic'),
            command=self.controller.open_summary_hall_sheet
        )
        hall_plan_btn.place(x=650, y=280)
        
        # Exit button
        exit_btn = tk.Button(
            self.root,
            text='Exit',
            bg='#87CEEB',
            fg='#FFFFFF',
            font=("Comic Sans MS", 30, 'bold', 'italic'),
            command=self.controller.exit_application
        )
        exit_btn.place(x=500, y=480)
    
    def run(self):
        """Run the main application loop"""
        self.root.mainloop()
    
    def destroy(self):
        """Destroy the main window"""
        if self.root:
            self.root.destroy()