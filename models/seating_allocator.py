"""
Seating Allocator Model - Implements the round-robin seating allocation algorithm
"""
from models.exam_session import ExamSession


class SeatingAllocator:
    """
    SeatingAllocator class to implement round-robin seating allocation
    """
    def __init__(self, exam_session):
        """
        Initialize the SeatingAllocator
        
        Args:
            exam_session (ExamSession): Exam session with students and rooms
        """
        self.exam_session = exam_session
        # Initialize tracking variables for allocation
        self.odd_index = 0
        self.even_index = 0
    
    def allocate_seats(self):
        """
        Allocate seats using round-robin algorithm
        
        Returns:
            bool: True if allocation was successful, False otherwise
        """
        # Check if there are sufficient rooms
        if not self.exam_session.has_sufficient_capacity():
            return False
        
        # Group students by branch
        branch_groups = self.exam_session.get_students_by_branch()
        
        # Create even and odd lists for round-robin allocation
        even_list, odd_list = self._create_even_odd_lists(branch_groups)
        
        # Reset counters for allocation
        self.odd_index = 0
        self.even_index = 0
        
        # Allocate seats in each room
        for room in self.exam_session.rooms:
            # Clear any existing allocations
            room.clear_all_seats()
            
            # Skip if both lists are empty
            if not even_list and not odd_list:
                continue
            
            # Allocate seats using round-robin approach
            if len(branch_groups) > 1:
                self._allocate_alternating_seats(room, even_list, odd_list)
            else:
                # If only one branch, allocate sequentially
                self._allocate_sequential_seats(room, even_list + odd_list)
            
        return True
    
    def _create_even_odd_lists(self, branch_groups):
        """
        Create even and odd lists for round-robin allocation
        
        Args:
            branch_groups (dict): Dictionary with branch names as keys and lists of students as values
            
        Returns:
            tuple: (even_list, odd_list) of students
        """
        branch_wise_list = list(branch_groups.values())
        
        even_list = []
        odd_list = []
        
        # Distribute students between even and odd lists exactly as in original code
        for i, students in enumerate(branch_wise_list):
            if i == 0:
                even_list = students.copy()
            elif i == 1:
                odd_list = students.copy()
            else:
                if len(even_list) > len(odd_list):
                    odd_list.extend(students)
                else:
                    even_list.extend(students)
        
        # Ensure both lists have the same length by adding None for empty spots
        max_length = max(len(even_list), len(odd_list))
        even_list.extend([None] * (max_length - len(even_list)))
        odd_list.extend([None] * (max_length - len(odd_list)))
        
        return even_list, odd_list
    
    def _allocate_alternating_seats(self, room, even_list, odd_list):
        """
        Allocate seats in alternating pattern, exactly matching original algorithm
        
        Args:
            room (Room): Room to allocate seats in
            even_list (list): List of students for even columns
            odd_list (list): List of students for odd columns
        """
        # This follows the exact algorithm from the original dataframes.py
        columns = room.columns
        rows = room.rows
        
        # Calculate odd and even columns (same as original code)
        odd_cols = (columns + 1) // 2
        even_cols = columns - odd_cols
        
        # Allocate seats for odd columns (1, 3, 5, ...)
        for odd_col in range(1, odd_cols + 1):
            for odd_row in range(1, rows + 1):
                if self.odd_index < len(odd_list):
                    student = odd_list[self.odd_index]
                    if student is not None:  # Skip None values
                        # Adjust indices for 0-based system in our Room model
                        room.set_seat(odd_row - 1, (odd_col * 2 - 1) - 1, student)
                self.odd_index += 1
        
        # Allocate seats for even columns (2, 4, 6, ...)
        for even_col in range(1, even_cols + 1):
            for even_row in range(1, rows + 1):
                if self.even_index < len(even_list):
                    student = even_list[self.even_index]
                    if student is not None:  # Skip None values
                        # Adjust indices for 0-based system in our Room model
                        room.set_seat(even_row - 1, (even_col * 2) - 1, student)
                self.even_index += 1
    
    def _allocate_sequential_seats(self, room, students):
        """
        Allocate seats sequentially (for single branch)
        
        Args:
            room (Room): Room to allocate seats in
            students (list): List of students
        """
        # Following original algorithm for single branch
        k = 0
        for col in range(room.columns):
            for row in range(room.rows):
                if k < len(students) and students[k] is not None:
                    room.set_seat(row, col, students[k])
                k += 1
    
    def generate_statistics(self):
        """
        Generate statistics for the seating arrangement
        
        Returns:
            dict: Dictionary with statistics
        """
        stats = {
            'total_students': len(self.exam_session.students),
            'total_rooms': len(self.exam_session.rooms),
            'total_capacity': self.exam_session.get_total_capacity(),
            'rooms_stats': {},
            'branch_stats': {}
        }
        
        # Collect branch statistics
        for branch, students in self.exam_session.get_students_by_branch().items():
            stats['branch_stats'][branch] = len(students)
        
        # Collect room statistics
        for room in self.exam_session.rooms:
            room_stats = {
                'capacity': room.capacity,
                'assigned_seats': room.capacity - room.get_empty_seats_count(),
                'branch_distribution': {}
            }
            
            # Count students by branch in this room
            for row in range(room.rows):
                for col in range(room.columns):
                    student = room.get_seat(row, col)
                    if student and student.branch_name:
                        if student.branch_name not in room_stats['branch_distribution']:
                            room_stats['branch_distribution'][student.branch_name] = 0
                        room_stats['branch_distribution'][student.branch_name] += 1
            
            stats['rooms_stats'][room.room_no] = room_stats
        
        return stats