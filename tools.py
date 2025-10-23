import os
import platform
import webbrowser

system = platform.system()
def getchit():
    """
    Allows for character input for faster UI experience, no matter which platform the script is run on.
    """
    if system == "Windows":
        import msvcrt
        byte_input = msvcrt.getch()
        string_input = byte_input.decode('ascii')
        return string_input
    elif system == 'Linux' or system == "Darwin":
        import getch
        return getch.getch()
    else:
        print("Operating System not supported")
def clear_screen():
    """
    Allows for clear screen to occur no matter which platform the script is run on.
    """
    if system == "Windows":
        os.system('cls')
    elif system == "Linux" or system == "Darwin":
        os.system('clear')
    else:
        print("Operating System not supported")

def open_pdf(file_path):
    if os.path.exists(file_path):
        webbrowser.open_new(file_path)
        print(f"Opened PDF: {file_path}")
    else:
        print(f"Error: PDF file not found at {file_path}")
        
def lowerisUpper(input):
    """
    Converts inputs to uppercase, typically using this for single-character inputs.
    Allows me to ensure Alphabet characters are uppercased while numbers are left alone.
    You may ask "Why is this needed?"; a mystery to be certain.
    """
    if input.lower() == input:
        return input.upper()
    else:
        return input