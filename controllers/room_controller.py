"""
Room Controller - Manages room-related operations
"""
from models.room import Room
from models.data_manager import DataManager
from views.room_view import RoomView


class RoomController:
    """
    RoomController class to manage room operations
    """
    def __init__(self):
        """Initialize the room controller"""
        self.data_manager = DataManager()
        self.view = RoomView(self)
        self.rooms = []
        
        # Load initial rooms data
        self._load_rooms()
    
    def _load_rooms(self):
        """Load rooms from data source"""
        try:
            self.rooms = self.data_manager.load_rooms()
        except Exception:
            # Start with empty list if loading fails
            self.rooms = []
    
    def show_view(self):
        """Show the room management view"""
        self.view.show()
    
    def get_rooms(self):
        """
        Get the list of rooms
        
        Returns:
            list: List of Room objects
        """
        return self.rooms
    
    def add_room(self, room_no, rows, columns):
        """
        Add a new room
        
        Args:
            room_no (str): Room number
            rows (int): Number of rows
            columns (int): Number of columns
            
        Raises:
            ValueError: If room number already exists
        """
        # Check if room number already exists
        if any(room.room_no == room_no for room in self.rooms):
            raise ValueError(f"Room with number '{room_no}' already exists.")
        
        # Create new room
        room = Room(room_no, rows, columns)
        
        # Add to list
        self.rooms.append(room)
        
        # Save changes
        self._save_rooms()
    
    def update_room(self, original_room_no, room_no, rows, columns):
        """
        Update an existing room
        
        Args:
            original_room_no (str): Original room number for identification
            room_no (str): New room number
            rows (int): Number of rows
            columns (int): Number of columns
            
        Raises:
            ValueError: If room not found or new room number already exists
        """
        # Find the room to update
        room_to_update = None
        for room in self.rooms:
            if room.room_no == original_room_no:
                room_to_update = room
                break
        
        if room_to_update is None:
            raise ValueError(f"Room with number '{original_room_no}' not found.")
        
        # Check if new room number already exists (if changed)
        if room_no != original_room_no and any(room.room_no == room_no for room in self.rooms):
            raise ValueError(f"Room with number '{room_no}' already exists.")
        
        # Update room properties
        room_to_update.room_no = room_no
        room_to_update.rows = rows
        room_to_update.columns = columns
        
        # Reset seating grid with new dimensions
        room_to_update.seating_grid = [
            [None for _ in range(columns)] for _ in range(rows)
        ]
        
        # Save changes
        self._save_rooms()
    
    def delete_room(self, room_no):
        """
        Delete a room
        
        Args:
            room_no (str): Room number to delete
            
        Raises:
            ValueError: If room not found
        """
        # Find the room to delete
        room_to_delete = None
        for i, room in enumerate(self.rooms):
            if room.room_no == room_no:
                room_to_delete = i
                break
        
        if room_to_delete is None:
            raise ValueError(f"Room with number '{room_no}' not found.")
        
        # Remove the room
        del self.rooms[room_to_delete]
        
        # Save changes
        self._save_rooms()
    
    def _save_rooms(self):
        """Save rooms to data source"""
        try:
            self.data_manager.save_rooms(self.rooms)
        except Exception as e:
            raise ValueError(f"Failed to save rooms: {str(e)}")
    
    def get_total_capacity(self):
        """
        Get the total capacity of all rooms
        
        Returns:
            int: Total seating capacity
        """
        return sum(room.capacity for room in self.rooms)