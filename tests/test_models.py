# test_models.py - Test cases for model classes

import pytest
import os
import pandas as pd
from datetime import datetime

# Import your model classes
from models.student import Student
from models.room import Room
from models.exam_session import ExamSession
from models.seating_allocator import SeatingAllocator
from utils.constants import BRANCH_CODES

class TestStudent:
    def test_student_initialization(self):
        student = Student("21321A0401", year=2, semester=1, regulation="R21")
        
        assert student.hallticket_no == "21321A0401"
        assert student.year == 2
        assert student.semester == 1
        assert student.regulation == "R21"
        assert student.branch_name == "ECE"  # Should be derived from hallticket
    
    def test_get_branch_from_hallticket(self):
        # Test with CSE branch
        student = Student("21321A0501")
        assert student.branch_name == "CSE"
        
        # Test with EEE branch
        student = Student("21321A0201")
        assert student.branch_name == "EEE"
        
        # Test with invalid branch code
        student = Student("21321A9901")
        assert student.branch_name == ""
    
    def test_get_college_code(self):
        student = Student("21321A0401")
        assert student.get_college_code() == "32"

class TestRoom:
    def test_room_initialization(self):
        room = Room(101, 5, 5)
        
        assert room.room_no == 101
        assert room.rows == 5
        assert room.columns == 5
        assert room.capacity == 25
        
        # Check that seating grid is initialized with None values
        for row in range(5):
            for col in range(5):
                assert room.seating_grid[row][col] is None
    
    def test_set_and_get_seat(self):
        room = Room(101, 3, 3)
        student = Student("21321A0401")
        
        # Set a student to a seat
        room.set_seat(1, 2, student)
        
        # Get the student from the seat
        retrieved_student = room.get_seat(1, 2)
        
        assert retrieved_student == student
        assert room.is_seat_empty(0, 0)  # This seat should be empty
        assert not room.is_seat_empty(1, 2)  # This seat should be occupied
    
    def test_clear_all_seats(self):
        room = Room(101, 3, 3)
        student = Student("21321A0401")
        
        # Set a student to a seat
        room.set_seat(1, 2, student)
        
        # Clear all seats
        room.clear_all_seats()
        
        # Check that all seats are empty
        for row in range(3):
            for col in range(3):
                assert room.is_seat_empty(row, col)

class TestExamSession:
    def test_exam_session_initialization(self):
        exam_session = ExamSession(
            exam_name="Mid-Term Exam",
            date=datetime(2025, 7, 10),
            year=2,
            semester=1
        )
        
        assert exam_session.exam_name == "Mid-Term Exam"
        assert exam_session.date.day == 10
        assert exam_session.date.month == 7
        assert exam_session.date.year == 2025
        assert exam_session.year == 2
        assert exam_session.semester == 1
        assert len(exam_session.students) == 0
        assert len(exam_session.rooms) == 0
    
    def test_add_students_and_rooms(self):
        exam_session = ExamSession()
        
        # Create test students and rooms
        student1 = Student("21321A0401")
        student2 = Student("21321A0501")
        room1 = Room(101, 3, 3)
        room2 = Room("102", 4, 4)
        
        # Add students and rooms
        exam_session.add_student(student1)
        exam_session.add_students([student2])
        exam_session.add_room(room1)
        exam_session.add_rooms([room2])
        
        assert len(exam_session.students) == 2
        assert len(exam_session.rooms) == 2
        assert exam_session.get_total_capacity() == 9 + 16  # 3x3 + 4x4
    
    def test_has_sufficient_capacity(self):
        exam_session = ExamSession()
        
        # Add 10 students
        for i in range(10):
            exam_session.add_student(Student(f"21321A0{i+1:03d}"))
        
        # Add a room with capacity 9
        exam_session.add_room(Room(101, 3, 3))
        
        # Should not have sufficient capacity
        assert not exam_session.has_sufficient_capacity()
        assert exam_session.get_additional_capacity_needed() == 1
        
        # Add another room
        exam_session.add_room(Room("102", 2, 2))
        
        # Now should have sufficient capacity
        assert exam_session.has_sufficient_capacity()
        assert exam_session.get_additional_capacity_needed() == 0

class TestSeatingAllocator:
    def test_allocate_seats_single_branch(self):
        # Create an exam session with students all from the same branch
        exam_session = ExamSession()
        
        # Add 5 CSE students
        for i in range(5):
            exam_session.add_student(Student(f"21321A05{i+1:02d}"))
        
        # Add a room with capacity 9
        room = Room(101, 3, 3)
        exam_session.add_room(room)
        
        # Allocate seats
        allocator = SeatingAllocator(exam_session)
        result = allocator.allocate_seats()
        
        # Check allocation result
        assert result is True
        
        # Check that 5 seats are occupied
        occupied_count = 0
        for r in range(3):
            for c in range(3):
                if not room.is_seat_empty(r, c):
                    occupied_count += 1
        
        assert occupied_count == 5
    
    def test_allocate_seats_multiple_branches(self):
        # Create an exam session with students from different branches
        exam_session = ExamSession()
        
        # Add 3 CSE students
        for i in range(3):
            exam_session.add_student(Student(f"21321A05{i+1:02d}"))
        
        # Add 3 ECE students
        for i in range(3):
            exam_session.add_student(Student(f"21321A04{i+1:02d}"))
        
        # Add a room with capacity 9
        room = Room(101, 3, 3)
        exam_session.add_room(room)
        
        # Allocate seats
        allocator = SeatingAllocator(exam_session)
        result = allocator.allocate_seats()
        
        # Check allocation result
        assert result is True
        
        # Check that 6 seats are occupied
        occupied_count = 0
        for r in range(3):
            for c in range(3):
                if not room.is_seat_empty(r, c):
                    occupied_count += 1
        
        assert occupied_count == 6
        
        # Verify that no adjacent students are from the same branch
        # This is a simplification - the actual check should be more sophisticated
        branch_positions = {}
        for r in range(3):
            for c in range(3):
                student = room.get_seat(r, c)
                if student:
                    branch = student.branch_name
                    if branch not in branch_positions:
                        branch_positions[branch] = []
                    branch_positions[branch].append((r, c))
        
        # Check if any students from the same branch are adjacent (simplified check)
        has_adjacent_same_branch = False
        for branch, positions in branch_positions.items():
            for pos1 in positions:
                for pos2 in positions:
                    if pos1 != pos2:
                        r1, c1 = pos1
                        r2, c2 = pos2
                        # Check if adjacent horizontally or vertically
                        if (abs(r1 - r2) == 1 and c1 == c2) or (abs(c1 - c2) == 1 and r1 == r2):
                            has_adjacent_same_branch = True
        
        # This might fail depending on how the allocator actually works
        # Adjust the test if needed based on the specific implementation
        assert not has_adjacent_same_branch, "Students from same branch are adjacent"