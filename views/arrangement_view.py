"""
Arrangement View - Interface for generating and viewing seating arrangements
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime


class ArrangementView:
    """
    ArrangementView class for generating and viewing seating arrangements
    """
    def __init__(self, controller):
        """
        Initialize the arrangement view
        
        Args:
            controller: Arrangement controller instance
        """
        self.controller = controller
        self.window = None
        self.output_label = None
        self.entry_path = None
    
    def show(self):
        """Show the arrangement view window"""
        if self.window is not None and self.window.winfo_exists():
            # If window already exists, just focus it
            self.window.focus_force()
            return
        
        # Create new window
        self.window = tk.Toplevel()
        self.window.title("Hall Sheet & Summary Sheet")
        self.window.geometry("900x600+10+10")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        # Configure window style
        self.window.configure(
            background='#E6E6FA',
            bd=15,
            highlightthickness=10,
            highlightbackground="#800080",
            highlightcolor="#E6E6FA",
            relief="groove"
        )
        
        # Setup the UI components
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface components"""
        # Add header label
        header_label = tk.Label(
            self.window,
            text="Browse the path for Excel Sheet",
            fg='#87CEEB',
            bg='white',
            font=("Comic Sans MS", 15, 'bold', 'italic', "underline"),
            underline=0
        )
        header_label.pack(pady=10)
        
        # Create frame for file selection and action buttons
        frame_browse = tk.Frame(self.window, bg='#E6E6FA')
        frame_browse.pack(pady=50)
        
        # File path entry
        self.entry_path = tk.Entry(frame_browse, width=40, font=('Arial', 16))
        self.entry_path.grid(row=0, column=0, padx=5, pady=5)
        
        button_browse = tk.Button(
            frame_browse,
            text="Browse",
            command=self.browse_file,
            bg='white',
            fg='#87CEEB',
            font=("Comic Sans MS", 16, 'bold', 'italic')
        )
        button_browse.grid(row=0, column=1, padx=5, pady=5)
        
        # Check rooms button
        check_button = tk.Button(
            frame_browse,
            text='Check if Rooms\n are Sufficient',
            command=self.check_rooms_capacity,
            bg='white',
            fg='#87CEEB',
            font=("Comic Sans MS", 16, 'bold', 'italic')
        )
        check_button.grid(row=1, column=0, padx=5, pady=5)
        
        # Generate button
        generate_button = tk.Button(
            frame_browse,
            text="Halls And \nSummary Sheet",
            command=self.generate_seating_arrangement,
            bg='white',
            fg='#87CEEB',
            font=("Comic Sans MS", 16, 'bold', 'italic')
        )
        generate_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Output label
        self.output_label = tk.Label(
            frame_browse,
            text='',
            font=("Comic Sans MS", 16, 'bold', 'italic'),
            bg='#E6E6FA'
        )
        self.output_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # Exit button
        exit_button = tk.Button(
            frame_browse,
            text="Exit",
            command=self.close,
            bg='white',
            fg='#87CEEB',
            font=("Comic Sans MS", 16, 'bold', 'italic')
        )
        exit_button.grid(row=3, column=0, padx=5, pady=5)
    
    def browse_file(self):
        """Open file dialog to select Excel file"""
        file_path = filedialog.askopenfilename(
            parent=self.window,
            title="Select Student Data Excel File",
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        
        if file_path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, file_path)
    
    def check_rooms_capacity(self):
        """Check if available rooms have sufficient capacity"""
        input_path = self.entry_path.get()
        
        if not input_path:
            messagebox.showerror("Error", "Please select a student data file.")
            return
        
        try:
            result = self.controller.check_capacity(input_path)
            
            if result['sufficient']:
                self.output_label.configure(
                    text="no more rooms required",
                    fg='green'
                )
            else:
                self.output_label.configure(
                    text="still need more rooms",
                    fg='red'
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check capacity: {str(e)}")
            self.output_label.configure(text="")
    
    def generate_seating_arrangement(self):
        """Generate seating arrangement and save to Excel"""
        input_path = self.entry_path.get()
        
        if not input_path:
            messagebox.showerror("Error", "Please select a student data file.")
            return
        
        try:
            # First, check if capacity is sufficient
            result = self.controller.check_capacity(input_path)
            
            if not result['sufficient']:
                if not messagebox.askyesno(
                    "Warning",
                    "Available rooms are NOT sufficient for all students.\n"
                    "Do you want to continue anyway?"
                ):
                    return
            
            # Generate the seating arrangement
            output_files = self.controller.generate_seating_arrangement(input_path)
            
            # Open the generated files
            self.controller.open_files(output_files.values())
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate seating arrangement: {str(e)}")
            self.output_label.configure(text="")
    
    def close(self):
        """Close the arrangement view window"""
        if self.window:
            self.window.destroy()
            self.window = None