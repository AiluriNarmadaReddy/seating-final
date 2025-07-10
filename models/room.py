"""
Room Model - Represents examination rooms/halls
"""


class Room:
    """
    Room class to represent an examination hall
    """
    def __init__(self, room_no, rows, columns):
        """
        Initialize a Room object
        
        Args:
            room_no (str): Room identifier
            rows (int): Number of rows in the room
            columns (int): Number of columns in the room
        """
        self.room_no = room_no
        self.rows = rows
        self.columns = columns
        
        # Initialize the seating grid with None values
        self.seating_grid = [[None for _ in range(columns)] for _ in range(rows)]
    
    @property
    def capacity(self):
        """Total seating capacity of the room"""
        return self.rows * self.columns
    
    def set_seat(self, row, column, student):
        """
        Assign a student to a specific seat
        
        Args:
            row (int): Row index (0-based)
            column (int): Column index (0-based)
            student: Student object or hallticket number
        
        Raises:
            IndexError: If row or column is out of bounds
        """
        if row < 0 or row >= self.rows or column < 0 or column >= self.columns:
            raise IndexError(f"Seat position ({row}, {column}) is out of bounds")
        
        self.seating_grid[row][column] = student
    
    def get_seat(self, row, column):
        """
        Get the student assigned to a specific seat
        
        Args:
            row (int): Row index (0-based)
            column (int): Column index (0-based)
            
        Returns:
            Student or None: The student assigned to the seat or None if empty
            
        Raises:
            IndexError: If row or column is out of bounds
        """
        if row < 0 or row >= self.rows or column < 0 or column >= self.columns:
            raise IndexError(f"Seat position ({row}, {column}) is out of bounds")
        
        return self.seating_grid[row][column]
    
    def is_seat_empty(self, row, column):
        """
        Check if a specific seat is empty
        
        Args:
            row (int): Row index (0-based)
            column (int): Column index (0-based)
            
        Returns:
            bool: True if the seat is empty, False otherwise
            
        Raises:
            IndexError: If row or column is out of bounds
        """
        return self.get_seat(row, column) is None
    
    def get_empty_seats_count(self):
        """
        Count the number of empty seats in the room
        
        Returns:
            int: Number of empty seats
        """
        count = 0
        for row in range(self.rows):
            for col in range(self.columns):
                if self.is_seat_empty(row, col):
                    count += 1
        return count
    
    def clear_all_seats(self):
        """Clear all seat assignments in the room"""
        self.seating_grid = [[None for _ in range(self.columns)] for _ in range(self.rows)]
    
    def __str__(self):
        """String representation of the room"""
        return f"Room {self.room_no} ({self.rows}x{self.columns})"
    
    def __repr__(self):
        """Representation of the room object"""
        return f"Room('{self.room_no}', {self.rows}, {self.columns})"