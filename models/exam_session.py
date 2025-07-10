"""
Exam Session Model - Represents an examination session with rooms and students
"""
import time
from datetime import datetime


class ExamSession:
    """
    ExamSession class to represent a complete exam session
    """
    def __init__(self, exam_name=None, date=None, year=None, semester=None):
        """
        Initialize an ExamSession object
        
        Args:
            exam_name (str, optional): Name of the examination
            date (datetime, optional): Date of the examination
            year (int, optional): Year of study for the exam
            semester (int, optional): Semester for the exam
        """
        self.exam_name = exam_name
        
        # Set date to current date if not provided
        if date is None:
            self.date = datetime.now()
        else:
            self.date = date
            
        self.year = year
        self.semester = semester
        
        # Lists to store students and rooms
        self.students = []
        self.rooms = []
    
    def add_student(self, student):
        """
        Add a student to the exam session
        
        Args:
            student: Student object
        """
        self.students.append(student)
    
    def add_students(self, students):
        """
        Add multiple students to the exam session
        
        Args:
            students (list): List of Student objects
        """
        self.students.extend(students)
    
    def add_room(self, room):
        """
        Add a room to the exam session
        
        Args:
            room: Room object
        """
        self.rooms.append(room)
    
    def add_rooms(self, rooms):
        """
        Add multiple rooms to the exam session
        
        Args:
            rooms (list): List of Room objects
        """
        self.rooms.extend(rooms)
    
    def remove_student(self, hallticket_no):
        """
        Remove a student from the exam session
        
        Args:
            hallticket_no (str): Hall ticket number of the student to remove
            
        Returns:
            bool: True if student was removed, False if not found
        """
        for i, student in enumerate(self.students):
            if student.hallticket_no == hallticket_no:
                del self.students[i]
                return True
        return False
    
    def remove_room(self, room_no):
        """
        Remove a room from the exam session
        
        Args:
            room_no (str): Room number to remove
            
        Returns:
            bool: True if room was removed, False if not found
        """
        for i, room in enumerate(self.rooms):
            if room.room_no == room_no:
                del self.rooms[i]
                return True
        return False
    
    def get_total_capacity(self):
        """
        Get the total seating capacity across all rooms
        
        Returns:
            int: Total seating capacity
        """
        return sum(room.capacity for room in self.rooms)
    
    def has_sufficient_capacity(self):
        """
        Check if there is sufficient seating capacity for all students
        
        Returns:
            bool: True if there is sufficient capacity, False otherwise
        """
        return self.get_total_capacity() >= len(self.students)
    
    def get_additional_capacity_needed(self):
        """
        Calculate additional capacity needed if current capacity is insufficient
        
        Returns:
            int: Additional seats needed (0 if capacity is sufficient)
        """
        if self.has_sufficient_capacity():
            return 0
        return len(self.students) - self.get_total_capacity()
    
    def get_formatted_date(self, format_str="%d_%b_%y"):
        """
        Get formatted date string for the exam session
        
        Args:
            format_str (str, optional): Format string for the date
            
        Returns:
            str: Formatted date string
        """
        return self.date.strftime(format_str)
    
    def get_students_by_branch(self):
        """
        Group students by branch
        
        Returns:
            dict: Dictionary with branch names as keys and lists of students as values
        """
        branch_dict = {}
        for student in self.students:
            if student.branch_name not in branch_dict:
                branch_dict[student.branch_name] = []
            branch_dict[student.branch_name].append(student)
        return branch_dict
    
    def __str__(self):
        """String representation of the exam session"""
        date_str = self.get_formatted_date("%d %b %Y")
        return f"Exam Session: {self.exam_name} on {date_str} ({len(self.students)} students, {len(self.rooms)} rooms)"