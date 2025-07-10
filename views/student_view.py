"""
Student View - Interface for importing and viewing student data
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class StudentView:
    """
    StudentView class for importing and viewing student data
    """
    def __init__(self, controller):
        """
        Initialize the student data view
        
        Args:
            controller: Student controller instance
        """
        self.controller = controller
        self.window = None
        self.student_tree = None
        self.file_path_var = None
    
    def show(self):
        """Show the student data window"""
        if self.window is not None and self.window.winfo_exists():
            # If window already exists, just focus it
            self.window.focus_force()
            return
        
        # Create new window
        self.window = tk.Toplevel()
        self.window.title("Student Data Import")
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
            text="Import Student Data",
            fg='#87CEEB',
            bg='white',
            font=("Comic Sans MS", 15, 'bold', 'italic', "underline"),
            underline=0
        )
        header_label.pack(pady=10)
        
        # Create frame for file selection
        file_frame = tk.Frame(self.window, bg='#E6E6FA')
        file_frame.pack(pady=10)
        
        # File path input field
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(
            file_frame,
            width=40,
            font=('Arial', 16),
            textvariable=self.file_path_var
        )
        file_entry.grid(row=0, column=0, padx=5, pady=5)
        
        # Browse button
        browse_button = tk.Button(
            file_frame,
            text="Browse",
            command=self.browse_file,
            bg='white',
            fg='#87CEEB',
            font=("Comic Sans MS", 16, 'bold', 'italic')
        )
        browse_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Import button
        import_button = tk.Button(
            file_frame,
            text="Import Data",
            command=self.import_data,
            bg='white',
            fg='#87CEEB',
            font=("Comic Sans MS", 16, 'bold', 'italic')
        )
        import_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Create frame for student list
        list_frame = tk.Frame(self.window, bg='#E6E6FA')
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Student list treeview
        self.student_tree = ttk.Treeview(list_frame)
        self.student_tree["columns"] = ("Hallticket No", "Year", "Semester", "Regulation", "Branch")
        
        # Hide the default first column
        self.student_tree.column("#0", width=0, stretch=tk.NO)
        
        # Configure visible columns
        column_widths = {
            "Hallticket No": 150,
            "Year": 80,
            "Semester": 80,
            "Regulation": 100,
            "Branch": 150
        }
        
        for col, width in column_widths.items():
            self.student_tree.column(col, anchor=tk.CENTER, width=width)
            self.student_tree.heading(col, text=col)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.student_tree.yview
        )
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.student_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create frame for action buttons
        button_frame = tk.Frame(self.window, bg='#E6E6FA')
        button_frame.pack(pady=10)
        
        # Exit button
        exit_button = tk.Button(
            button_frame,
            text="Close",
            command=self.close,
            bg='white',
            fg='#87CEEB',
            font=("Comic Sans MS", 16, 'bold', 'italic')
        )
        exit_button.pack(pady=5)
    
    def browse_file(self):
        """Open file dialog to select Excel file"""
        file_path = filedialog.askopenfilename(
            parent=self.window,
            title="Select Excel File",
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
    
    def import_data(self):
        """Import student data from the selected file"""
        file_path = self.file_path_var.get()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file to import.")
            return
        
        try:
            # Import the data via controller
            students = self.controller.import_student_data(file_path)
            
            # Update the treeview
            self.refresh_student_list(students)
            
            messagebox.showinfo(
                "Success",
                f"Successfully imported {len(students)} students."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {str(e)}")
    
    def refresh_student_list(self, students=None):
        """
        Refresh the student list with current data
        
        Args:
            students (list, optional): List of Student objects
        """
        # Clear existing items
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        # If students not provided, get them from controller
        if students is None:
            students = self.controller.get_students()
        
        # Add students to the treeview
        for student in students:
            self.student_tree.insert(
                "",
                tk.END,
                text="",
                values=(
                    student.hallticket_no,
                    student.year,
                    student.semester,
                    student.regulation,
                    student.branch_name
                )
            )
    
    def close(self):
        """Close the student data window"""
        if self.window:
            self.window.destroy()
            self.window = None