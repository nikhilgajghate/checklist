import subprocess
import sys
import os

def build_executable():
    """Build the checklist application as an executable"""
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window
        "--name=ChecklistApp",  # Name of the executable
        "--icon=src/icon.ico",  # Icon (if available)
        "--add-data=src;src",  # Include source files
        "src/checklist_app.py"
    ]
    
    # Remove icon option if icon doesn't exist
    if not os.path.exists("src/icon.ico"):
        cmd = [arg for arg in cmd if not arg.startswith("--icon")]
    
    try:
        print("Building executable...")
        print(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("Build completed successfully!")
        print("Executable created in: dist/ChecklistApp.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("PyInstaller not found. Please install it with: pip install pyinstaller")
        return False
    
    return True

if __name__ == "__main__":
    build_executable() 