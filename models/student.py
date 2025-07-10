"""
Student Model - Represents student data for exam seating arrangement
"""
from utils.constants import BRANCH_CODES


class Student:
    """
    Student class to represent a student in the seating arrangement system
    """
    def __init__(self, hallticket_no, year=None, semester=None, regulation=None, branch_name=None):
        """
        Initialize a Student object
        
        Args:
            hallticket_no (str): Student's hall ticket number
            year (int, optional): Year of study
            semester (int, optional): Current semester
            regulation (str, optional): Regulation code/year
            branch_name (str, optional): Name of the branch/department
        """
        self.hallticket_no = hallticket_no
        self.year = year
        self.semester = semester
        self.regulation = regulation
        
        # Set branch name based on hallticket if not provided
        if branch_name is None and len(hallticket_no) == 10:
            self.branch_name = self._get_branch_from_hallticket()
        else:
            self.branch_name = branch_name
    
    def _get_branch_from_hallticket(self):
        """
        Extract branch name from hallticket number
        
        Returns:
            str: Branch name or empty string if branch code not found
        """
        if len(self.hallticket_no) == 10:
            branch_code = self.hallticket_no[6:8]
            if branch_code in BRANCH_CODES:
                return BRANCH_CODES[branch_code]
        return ""
    
    def get_branch_code(self):
        """
        Get the branch code from the hallticket number
        
        Returns:
            str: Branch code or empty string if not found
        """
        if len(self.hallticket_no) == 10:
            return self.hallticket_no[6:8]
        return ""
    
    def get_college_code(self):
        """
        Get the college code from the hallticket number
        
        Returns:
            str: College code or empty string if not found
        """
        if len(self.hallticket_no) == 10:
            return self.hallticket_no[2:4]
        return ""
    
    def __str__(self):
        """String representation of the student"""
        return f"{self.hallticket_no} ({self.branch_name})"
    
    def __repr__(self):
        """Representation of the student object"""
        return f"Student('{self.hallticket_no}', {self.year}, {self.semester}, '{self.regulation}', '{self.branch_name}')"