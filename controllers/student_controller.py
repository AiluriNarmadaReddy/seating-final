"""
Student Controller - Manages student-related operations
"""
from models.student import Student
from models.data_manager import DataManager
from views.student_view import StudentView


class StudentController:
    """
    StudentController class to manage student operations
    """
    def __init__(self):
        """Initialize the student controller"""
        self.data_manager = DataManager()
        self.view = StudentView(self)
        self.students = []
    
    def show_view(self):
        """Show the student data view"""
        self.view.show()
    
    def get_students(self):
        """
        Get the list of students
        
        Returns:
            list: List of Student objects
        """
        return self.students
    
    def import_student_data(self, file_path):
        """
        Import student data from Excel file
        
        Args:
            file_path (str): Path to the Excel file
            
        Returns:
            list: List of imported Student objects
            
        Raises:
            ValueError: If import fails
        """
        try:
            # Import students using data manager
            self.students = self.data_manager.load_student_data(file_path)
            return self.students
        except Exception as e:
            raise ValueError(f"Failed to import student data: {str(e)}")
    
    def get_student_count(self):
        """
        Get the number of students
        
        Returns:
            int: Number of students
        """
        return len(self.students)
    
    def group_students_by_branch(self):
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
    
    def group_students_by_regulation(self):
        """
        Group students by regulation
        
        Returns:
            dict: Dictionary with regulation codes as keys and lists of students as values
        """
        regulation_dict = {}
        for student in self.students:
            if student.regulation not in regulation_dict:
                regulation_dict[student.regulation] = []
            regulation_dict[student.regulation].append(student)
        return regulation_dict
    
    def get_unique_years(self):
        """
        Get unique years from student data
        
        Returns:
            list: List of unique years
        """
        return sorted(list(set(student.year for student in self.students if student.year)))
    
    def get_unique_semesters(self):
        """
        Get unique semesters from student data
        
        Returns:
            list: List of unique semesters
        """
        return sorted(list(set(student.semester for student in self.students if student.semester)))
    
    def set_students(self, students):
        """
        Set the list of students
        
        Args:
            students (list): List of Student objects
        """
        self.students = students