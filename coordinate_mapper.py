# ==========================================
# PROJECT LIBRARIES (All loaded)
# ==========================================
import pyautogui          # The "ghost" that will move the mouse and type
import pygetwindow as gw  # To find and focus on software windows
import customtkinter as ctk # To create the visual GUI at the end
import time               # To provide necessary pauses between clicks
import subprocess         # To open the software if it's closed

# ==========================================
# MAPPING SCRIPT (COORDINATE RADAR)
# ==========================================

def start_radar():
    print("Starting Mouse Radar...")
    print("Move the mouse over the color buttons in your setup's software.")
    print("Press Ctrl+C here in the terminal to stop the script.\n")

    try:
        while True:
            # Gets the current mouse position on the screen
            x, y = pyautogui.position()
            
            # Formats the output to keep the terminal clean, updating on the same line
            position = f"Current Position -> X: {x:>4} | Y: {y:>4}"
            print(position, end='\r')
            
            # A short pause to avoid frying the CPU with an infinite loop
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nRadar finished! Hope you wrote down the coordinates.")

# Runs the radar
if __name__ == "__main__":
    start_radar()
