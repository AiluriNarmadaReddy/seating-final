"""
Arrangement Controller - Manages seating arrangement operations
"""
import os
import subprocess
from datetime import datetime

from models.exam_session import ExamSession
from models.seating_allocator import SeatingAllocator
from models.data_manager import DataManager
from views.arrangement_view import ArrangementView


class ArrangementController:
    """
    ArrangementController class to manage seating arrangement operations
    """
    def __init__(self, room_controller, student_controller):
        """
        Initialize the arrangement controller
        
        Args:
            room_controller: Room controller instance
            student_controller: Student controller instance
        """
        self.room_controller = room_controller
        self.student_controller = student_controller
        self.data_manager = DataManager()
        self.view = ArrangementView(self)
        self.exam_session = None
    
    def show_view(self):
        """Show the arrangement view"""
        self.view.show()
    
    def check_capacity(self, student_file_path):
        """
        Check if available rooms have sufficient capacity for all students
        
        Args:
            student_file_path (str): Path to student data file
            
        Returns:
            dict: Dictionary with capacity check results
            
        Raises:
            ValueError: If capacity check fails
        """
        try:
            # Import student data
            students = self.data_manager.load_student_data(student_file_path)
            
            # Get rooms
            rooms = self.room_controller.get_rooms()
            
            # Calculate totals
            total_students = len(students)
            total_capacity = sum(room.capacity for room in rooms)
            
            # Check if capacity is sufficient
            sufficient = total_capacity >= total_students
            
            # Calculate extra or needed capacity
            if sufficient:
                extra_capacity = total_capacity - total_students
                additional_needed = 0
            else:
                extra_capacity = 0
                additional_needed = total_students - total_capacity
            
            # Return results
            return {
                'sufficient': sufficient,
                'total_students': total_students,
                'total_capacity': total_capacity,
                'extra_capacity': extra_capacity,
                'additional_needed': additional_needed
            }
            
        except Exception as e:
            raise ValueError(f"Failed to check capacity: {str(e)}")
    
    def generate_seating_arrangement(self, student_file_path):
        """
        Generate seating arrangement based on student data and available rooms
        
        Args:
            student_file_path (str): Path to student data file
            
        Returns:
            dict: Dictionary with paths to generated files
            
        Raises:
            ValueError: If seating arrangement generation fails
        """
        try:
            # Create exam session
            self.exam_session = ExamSession(
                exam_name="JNTU External Examination",
                date=datetime.now()
            )
            
            # Load students
            students = self.data_manager.load_student_data(student_file_path)
            self.exam_session.add_students(students)
            
            # Get student year and semester if available
            if students and students[0].year is not None:
                self.exam_session.year = students[0].year
            if students and students[0].semester is not None:
                self.exam_session.semester = students[0].semester
            
            # Load rooms
            rooms = self.room_controller.get_rooms()
            self.exam_session.add_rooms(rooms)
            
            # Create seating allocator
            allocator = SeatingAllocator(self.exam_session)
            
            # Allocate seats
            if not allocator.allocate_seats():
                raise ValueError("Failed to allocate seats. Insufficient room capacity.")
            
            # Generate date-based filenames
            date_str = self.exam_session.get_formatted_date("%d_%b_%y")
            seating_file = f"{date_str}.xlsx"  # Match original naming convention
            summary_file = f"{date_str}_summary.xlsx"
            out_sheet_file = f"{date_str}_out_sheet.xlsx"
            all_roll_file = f"{date_str}_all_roll.xlsx"
            
            # First save all students to all_roll.xlsx - this is needed for compatibility
            # with the original code that uses this file
            self._save_all_students(all_roll_file)
            
            # Save seating arrangement
            self.data_manager.save_seating_arrangement(
                self.exam_session,
                seating_file
            )
            
            # Save summary
            self.data_manager.save_summary(
                self.exam_session,
                summary_file
            )
            
            # Save out sheet
            self.data_manager.save_out_sheet(
                self.exam_session,
                out_sheet_file
            )
            
            # Return file paths
            return {
                'seating': seating_file,
                'summary': summary_file,
                'out_sheet': out_sheet_file,
                'all_roll': all_roll_file
            }
            
        except Exception as e:
            raise ValueError(f"Failed to generate seating arrangement: {str(e)}")
    
    def _save_all_students(self, file_path):
        """
        Save all students to Excel file (needed for compatibility)
        
        Args:
            file_path (str): Path to save the file
            
        Raises:
            ValueError: If saving fails
        """
        try:
            # Create DataFrame
            data = []
            for student in self.exam_session.students:
                data.append({
                    'Hallticketno': student.hallticket_no,
                    'Year': student.year,
                    'Semester': student.semester,
                    'Regulation': student.regulation,
                    'Branch Name': student.branch_name,
                    'index': 0  # Will be updated below
                })
            
            # Convert to DataFrame
            import pandas as pd
            df = pd.DataFrame(data)
            
            # Add index
            df['index'] = range(1, len(df) + 1)
            
            # Save to Excel
            with pd.ExcelWriter(file_path) as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
                
        except Exception as e:
            raise ValueError(f"Failed to save all students: {str(e)}")
    
    def open_files(self, file_paths):
        """
        Open generated files using the default application
        
        Args:
            file_paths (list): List of file paths to open
            
        Raises:
            ValueError: If file opening fails
        """
        try:
            for file_path in file_paths:
                # Check if file exists
                if not os.path.exists(file_path):
                    continue
                    
                # Open file with default application
                if os.name == 'nt':  # Windows
                    os.startfile(file_path)
                elif os.name == 'posix':  # macOS or Linux
                    subprocess.call(('open' if os.uname().sysname == 'Darwin' else 'xdg-open', file_path))
                    
        except Exception as e:
            raise ValueError(f"Failed to open files: {str(e)}")