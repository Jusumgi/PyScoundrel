import os
import platform
import webbrowser
import json

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

def saveLog(data):
    # If the folder isn't created yet, then create it.
    folder_path = "save/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    save_file = "save/score_history.json"

    # If the file doesn't exist, create the file, add data(a list) into an empty list.
    # If the file exists, read the file and load it's contents into 'data' so that a new list can be appended, then written to the save file.

    if os.path.exists(save_file):
        with open(save_file, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []    
        data.append(data)
        with open(save_file, "w") as file:
            json.dump(data, file, indent=4)    
    else:
        with open(save_file, "w") as file:
             file.write("[")
             json.dump(data, file)
             file.write("]")