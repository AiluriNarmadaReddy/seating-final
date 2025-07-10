"""
Room View - Interface for managing examination rooms
"""
import tkinter as tk
from tkinter import ttk, messagebox


class RoomView:
    """
    RoomView class for managing examination rooms
    """
    def __init__(self, controller):
        """
        Initialize the room management view
        
        Args:
            controller: Room controller instance
        """
        self.controller = controller
        self.window = None
        self.room_tree = None
        self.add_popup = None
        self.edit_popup = None
    
    def show(self):
        """Show the room management window"""
        if self.window is not None and self.window.winfo_exists():
            # If window already exists, just focus it
            self.window.focus_force()
            return
        
        # Create new window
        self.window = tk.Toplevel()
        self.window.title("Examination Rooms")
        self.window.geometry("700x500+10+10")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        # Setup the UI components
        self._setup_ui()
        
        # Load room data
        self.refresh_room_list()
    
    def _setup_ui(self):
        """Set up the user interface components"""
        # Create treeview for room list
        self.room_tree = ttk.Treeview(self.window)
        
        # Configure columns
        self.room_tree["columns"] = ("Room No", "Rows", "Columns", "Capacity")
        
        # Hide the default first column
        self.room_tree.column("#0", width=0, stretch=tk.NO)
        
        # Configure visible columns
        for col in self.room_tree["columns"]:
            self.room_tree.column(col, anchor=tk.CENTER, width=100)
            self.room_tree.heading(col, text=col)
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        # Add the treeview to the window
        self.room_tree.pack(expand=True, fill=tk.BOTH)
        
        # Create a frame for buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(side=tk.BOTTOM, pady=(10, 0))
        
        # Add buttons
        add_button = ttk.Button(
            button_frame, 
            text="Add", 
            command=self.show_add_dialog
        )
        edit_button = ttk.Button(
            button_frame, 
            text="Edit", 
            command=self.show_edit_dialog
        )
        delete_button = ttk.Button(
            button_frame, 
            text="Delete", 
            command=self.delete_selected_room
        )
        exit_button = ttk.Button(
            button_frame, 
            text="Exit", 
            command=self.close
        )
        
        # Pack buttons with spacing
        add_button.pack(side=tk.LEFT, padx=10)
        edit_button.pack(side=tk.LEFT, padx=10)
        delete_button.pack(side=tk.LEFT, padx=10)
        exit_button.pack(side=tk.LEFT, padx=10)
        
        # Add selection event binding
        self.room_tree.bind("<<TreeviewSelect>>", self.on_room_selected)
    
    def refresh_room_list(self):
        """Refresh the room list with current data"""
        # Clear existing items
        for item in self.room_tree.get_children():
            self.room_tree.delete(item)
        
        # Add rooms to the treeview
        rooms = self.controller.get_rooms()
        for room in rooms:
            self.room_tree.insert(
                "", 
                tk.END, 
                text="", 
                values=(room.room_no, room.rows, room.columns, room.capacity)
            )
    
    def show_add_dialog(self):
        """Show dialog for adding a new room"""
        if self.add_popup is not None and self.add_popup.winfo_exists():
            # If dialog already exists, just focus it
            self.add_popup.focus_force()
            return
        
        # Create new dialog
        self.add_popup = tk.Toplevel(self.window)
        self.add_popup.title("Add Room")
        self.add_popup.geometry("+10+10")
        self.add_popup.protocol("WM_DELETE_WINDOW", self._close_add_dialog)
        
        # Variables for form fields
        room_no_var = tk.StringVar(value="")
        rows_var = tk.IntVar(value=5)
        columns_var = tk.IntVar(value=5)
        
        # Create form fields
        room_no_label = ttk.Label(self.add_popup, text="Room No.")
        room_no_entry = ttk.Entry(self.add_popup, textvariable=room_no_var)
        rows_label = ttk.Label(self.add_popup, text="Rows")
        rows_spinbox = ttk.Spinbox(
            self.add_popup, 
            from_=1, 
            to=50, 
            textvariable=rows_var
        )
        columns_label = ttk.Label(self.add_popup, text="Columns")
        columns_spinbox = ttk.Spinbox(
            self.add_popup, 
            from_=1, 
            to=50, 
            textvariable=columns_var
        )
        
        # Add form fields to dialog
        room_no_label.pack(pady=(10, 0))
        room_no_entry.pack(pady=(0, 10))
        rows_label.pack(pady=(10, 0))
        rows_spinbox.pack(pady=(0, 10))
        columns_label.pack(pady=(10, 0))
        columns_spinbox.pack(pady=(0, 10))
        
        # Add save button
        save_button = ttk.Button(
            self.add_popup,
            text="Save",
            command=lambda: self.save_new_room(
                room_no_var.get(),
                rows_var.get(),
                columns_var.get()
            )
        )
        save_button.pack(pady=10)
    
    def save_new_room(self, room_no, rows, columns):
        """
        Save a new room
        
        Args:
            room_no (str): Room number
            rows (int): Number of rows
            columns (int): Number of columns
        """
        # Validate input
        if not room_no:
            messagebox.showerror("Error", "Room number cannot be empty.")
            return
        
        # Try to add the room
        try:
            self.controller.add_room(room_no, rows, columns)
            self.refresh_room_list()
            self._close_add_dialog()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _close_add_dialog(self):
        """Close the add room dialog"""
        if self.add_popup:
            self.add_popup.destroy()
            self.add_popup = None
    
    def show_edit_dialog(self):
        """Show dialog for editing a room"""
        # Get the selected room
        selected_item = self.room_tree.focus()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a room to edit.")
            return
        
        # Get room data
        values = self.room_tree.item(selected_item)["values"]
        room_no, rows, columns, _ = values
        
        if self.edit_popup is not None and self.edit_popup.winfo_exists():
            # If dialog already exists, just focus it
            self.edit_popup.focus_force()
            return
        
        # Create new dialog
        self.edit_popup = tk.Toplevel(self.window)
        self.edit_popup.title("Edit Room")
        self.edit_popup.geometry("+10+10")
        self.edit_popup.protocol("WM_DELETE_WINDOW", self._close_edit_dialog)
        
        # Variables for form fields
        room_no_var = tk.StringVar(value=room_no)
        rows_var = tk.IntVar(value=rows)
        columns_var = tk.IntVar(value=columns)
        
        # Create form fields
        room_no_label = ttk.Label(self.edit_popup, text="Room No.")
        room_no_entry = ttk.Entry(self.edit_popup, textvariable=room_no_var)
        rows_label = ttk.Label(self.edit_popup, text="Rows")
        rows_spinbox = ttk.Spinbox(
            self.edit_popup, 
            from_=1, 
            to=50, 
            textvariable=rows_var
        )
        columns_label = ttk.Label(self.edit_popup, text="Columns")
        columns_spinbox = ttk.Spinbox(
            self.edit_popup, 
            from_=1, 
            to=50, 
            textvariable=columns_var
        )
        
        # Add form fields to dialog
        room_no_label.pack(pady=(10, 0))
        room_no_entry.pack(pady=(0, 10))
        rows_label.pack(pady=(10, 0))
        rows_spinbox.pack(pady=(0, 10))
        columns_label.pack(pady=(10, 0))
        columns_spinbox.pack(pady=(0, 10))
        
        # Add save button
        save_button = ttk.Button(
            self.edit_popup,
            text="Save",
            command=lambda: self.save_edited_room(
                room_no,  # Original room number for identification
                room_no_var.get(),
                rows_var.get(),
                columns_var.get()
            )
        )
        save_button.pack(pady=10)
    
    def save_edited_room(self, original_room_no, room_no, rows, columns):
        """
        Save changes to an existing room
        
        Args:
            original_room_no (str): Original room number for identification
            room_no (str): New room number
            rows (int): Number of rows
            columns (int): Number of columns
        """
        # Validate input
        if not room_no:
            messagebox.showerror("Error", "Room number cannot be empty.")
            return
        
        # Try to update the room
        try:
            self.controller.update_room(original_room_no, room_no, rows, columns)
            self.refresh_room_list()
            self._close_edit_dialog()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _close_edit_dialog(self):
        """Close the edit room dialog"""
        if self.edit_popup:
            self.edit_popup.destroy()
            self.edit_popup = None
    
    def delete_selected_room(self):
        """Delete the selected room"""
        selected_item = self.room_tree.focus()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a room to delete.")
            return
        
        # Get room number
        room_no = self.room_tree.item(selected_item)["values"][0]
        
        # Confirm deletion
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Room {room_no}?"
        ):
            try:
                self.controller.delete_room(room_no)
                self.refresh_room_list()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    def on_room_selected(self, event):
        """
        Handle room selection event
        
        Args:
            event: Selection event
        """
        # This can be extended if needed to handle selection actions
        pass
    
    def close(self):
        """Close the room management window"""
        if self.window:
            self.window.destroy()
            self.window = None
            self.add_popup = None
            self.edit_popup = None