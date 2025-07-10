"""
Main Controller - Coordinates the main application
"""
import sys
import os

from views.main_window import MainWindow
from controllers.room_controller import RoomController
from controllers.student_controller import StudentController
from controllers.arrangement_controller import ArrangementController
from controllers.report_controller import ReportController


class MainController:
    """
    MainController class to coordinate the main application
    """
    def __init__(self):
        """Initialize the main controller"""
        # Initialize view
        self.view = MainWindow(self)
        
        # Initialize sub-controllers
        self.room_controller = RoomController()
        self.student_controller = StudentController()
        self.arrangement_controller = ArrangementController(
            self.room_controller,
            self.student_controller
        )
        self.report_controller = ReportController(
            self.room_controller,
            self.student_controller
        )
    
    def run(self):
        """Run the main application"""
        self.view.run()
    
    def open_rooms(self):
        """Open the room management window"""
        self.room_controller.show_view()
    
    def open_summary_hall_sheet(self):
        """Open the summary and hall sheet window"""
        self.arrangement_controller.show_view()
    
    def exit_application(self):
        """Exit the application"""
        # Perform any cleanup if needed
        self.view.destroy()
        sys.exit(0)


def main():
    """Main entry point for the application"""
    # Create and run the main controller
    controller = MainController()
    controller.run()


if __name__ == "__main__":
    main()