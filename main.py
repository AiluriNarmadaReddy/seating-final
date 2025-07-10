"""
Main Entry Point - Starts the Exam Seating Plan Automation application
"""
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.main_controller import MainController


def main():
    """Main entry point for the application"""
    # Create required directories if they don't exist
    os.makedirs('resources', exist_ok=True)
    
    # Ensure original background image exists
    background_path = os.path.join('resources', 'background.jpg')
    if not os.path.exists(background_path):
        print(f"Warning: Background image not found at {background_path}")
        print("You may need to copy your background image to this location.")
    
    # Create and run the main controller
    controller = MainController()
    controller.run()


if __name__ == "__main__":
    main()