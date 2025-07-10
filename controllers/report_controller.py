"""
Report Controller - Manages report generation operations
"""
import os
from datetime import datetime

from models.exam_session import ExamSession
from models.data_manager import DataManager


class ReportController:
    """
    ReportController class to manage report generation operations
    """
    def __init__(self, room_controller, student_controller):
        """
        Initialize the report controller
        
        Args:
            room_controller: Room controller instance
            student_controller: Student controller instance
        """
        self.room_controller = room_controller
        self.student_controller = student_controller
        self.data_manager = DataManager()
    
    def generate_summary_report(self, exam_session=None):
        """
        Generate summary report of students by branch and regulation
        
        Args:
            exam_session (ExamSession, optional): Exam session instance
            
        Returns:
            str: Path to the generated file
            
        Raises:
            ValueError: If summary generation fails
        """
        try:
            # Create exam session if not provided
            if exam_session is None:
                exam_session = ExamSession(
                    exam_name="JNTU External Examination",
                    date=datetime.now()
                )
                
                # Add students
                exam_session.add_students(self.student_controller.get_students())
                
                # Get student year and semester if available
                students = self.student_controller.get_students()
                if students and students[0].year is not None:
                    exam_session.year = students[0].year
                if students and students[0].semester is not None:
                    exam_session.semester = students[0].semester
            
            # Generate date-based filename
            date_str = exam_session.get_formatted_date("%d_%b_%y")
            summary_file = f"{date_str}_summary.xlsx"
            
            # Save summary
            self.data_manager.save_summary(
                exam_session,
                summary_file
            )
            
            return summary_file
            
        except Exception as e:
            raise ValueError(f"Failed to generate summary report: {str(e)}")
    
    def generate_room_reports(self, exam_session=None):
        """
        Generate room-wise seating arrangement reports
        
        Args:
            exam_session (ExamSession, optional): Exam session instance
            
        Returns:
            str: Path to the generated file
            
        Raises:
            ValueError: If room report generation fails
        """
        try:
            # Create exam session if not provided
            if exam_session is None:
                exam_session = ExamSession(
                    exam_name="JNTU External Examination",
                    date=datetime.now()
                )
                
                # Add students
                exam_session.add_students(self.student_controller.get_students())
                
                # Add rooms
                exam_session.add_rooms(self.room_controller.get_rooms())
                
                # Get student year and semester if available
                students = self.student_controller.get_students()
                if students and students[0].year is not None:
                    exam_session.year = students[0].year
                if students and students[0].semester is not None:
                    exam_session.semester = students[0].semester
            
            # Generate date-based filename
            date_str = exam_session.get_formatted_date("%d_%b_%y")
            seating_file = f"{date_str}.xlsx"  # Use original filename format
            
            # Save seating arrangement
            self.data_manager.save_seating_arrangement(
                exam_session,
                seating_file
            )
            
            return seating_file
            
        except Exception as e:
            raise ValueError(f"Failed to generate room reports: {str(e)}")
    
    def open_file(self, file_path):
        """
        Open a file with the default application
        
        Args:
            file_path (str): Path to the file to open
            
        Raises:
            ValueError: If file opening fails
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise ValueError(f"File not found: {file_path}")
                
            # Open file with default application
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS or Linux
                import subprocess
                subprocess.call(('open' if os.uname().sysname == 'Darwin' else 'xdg-open', file_path))
                
        except Exception as e:
            raise ValueError(f"Failed to open file: {str(e)}")