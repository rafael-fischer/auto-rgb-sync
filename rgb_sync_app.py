import pyautogui
import pygetwindow as gw
import time
import customtkinter as ctk
import tkinter as tk
from tkinter import colorchooser 
from PIL import ImageGrab, ImageTk

# ==========================================
# 1. HELPER AND CONTROL FUNCTIONS
# ==========================================

def focus_window(window_title):
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            return False
        window = windows[0]
        if window.isMinimized:
            window.restore()
        window.activate()
        time.sleep(0.8)
        return True
    except Exception:
        return False

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def fill_field(x, y, value):
    pyautogui.moveTo(x, y, duration=0.3) 
    pyautogui.click()
    time.sleep(0.3) 
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.2)
    pyautogui.typewrite(str(value), interval=0.05) 
    time.sleep(0.2)

def fill_field_simple(x, y, value):
    pyautogui.moveTo(x, y, duration=0.3) 
    pyautogui.click()
    time.sleep(0.3) 
    pyautogui.typewrite(str(value), interval=0.05) 
    time.sleep(0.2)

# ==========================================
# 2. AUTOMATION SEQUENCES BY SOFTWARE
# ==========================================

def configure_mouse(r, g, b):
    # Insert the exact name of your mouse software window below
    if not focus_window("Mouse app"): return
    pyautogui.moveTo(1450, 474, duration=0.3)
    pyautogui.click()
    time.sleep(1.0)
    pyautogui.moveTo(1275, 593, duration=0.3)
    pyautogui.click()
    time.sleep(0.8)
    fill_field(1115, 730, r)
    fill_field(1196, 730, g)
    fill_field(1276, 730, b)
    pyautogui.moveTo(1285, 620, duration=0.3)
    pyautogui.click()
    time.sleep(0.5)

def configure_keyboard(r, g, b):
    # Insert the exact name of your keyboard software window below
    if not focus_window("Keyboard app"): return
    fill_field_simple(1056, 850, r)
    fill_field_simple(1168, 850, g)
    fill_field_simple(1280, 850, b)
    pyautogui.moveTo(1333, 900, duration=0.3)
    pyautogui.click()
    time.sleep(0.5)

def configure_motherboard(r, g, b):
    # Insert the exact name of your motherboard software window below
    if not focus_window("Motherboard app"): return
    fill_field(1215, 565, r)
    fill_field(1265, 565, g)
    fill_field(1313, 565, b)
    pyautogui.press('enter')
    time.sleep(0.5)

def apply_color_to_all(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    configure_mouse(r, g, b)
    configure_keyboard(r, g, b)
    configure_motherboard(r, g, b)

# ==========================================
# 3. COLOR PICKER (EYEDROPPER) LOGIC
# ==========================================

def open_color_picker():
    app.withdraw()
    time.sleep(0.3)
    
    screen_capture = ImageGrab.grab()
    
    overlay = ctk.CTkToplevel()
    overlay.attributes('-fullscreen', True)
    overlay.attributes('-topmost', True)
    overlay.config(cursor="crosshair")
    
    tk_image = ImageTk.PhotoImage(screen_capture)
    canvas = tk.Canvas(overlay, width=screen_capture.width, height=screen_capture.height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=tk_image)
    canvas.image = tk_image
    
    def capture_pixel(event):
        x, y = event.x, event.y
        r, g, b = screen_capture.getpixel((x, y))
        hex_color = f"#{r:02x}{g:02x}{b:02x}".upper()
        
        color_input.delete(0, 'end')
        color_input.insert(0, hex_color)
        preview_frame.configure(fg_color=hex_color)
        
        overlay.destroy()
        app.deiconify()
        
    def cancel_capture(event):
        overlay.destroy()
        app.deiconify()

    canvas.bind("<Button-1>", capture_pixel)
    overlay.bind("<Escape>", cancel_capture)

# ==========================================
# 4. GUI AND COLOR SPECTRUM
# ==========================================

def open_color_spectrum(event):
    """Opens the native Windows spectrum when clicking the color box"""
    current_color = color_input.get().strip() 
    
    if not current_color.startswith('#') or len(current_color) != 7:
        current_color = "#FFFFFF"

    chosen_color = colorchooser.askcolor(initialcolor=current_color, title="Choose Setup Color")
    
    if chosen_color[1]: 
        hex_color = chosen_color[1].upper() 
        
        color_input.delete(0, 'end')
        color_input.insert(0, hex_color)
        preview_frame.configure(fg_color=hex_color)

def start_automation():
    hex_color = color_input.get().strip()
    
    if not hex_color.startswith('#') or len(hex_color) != 7:
        status_label.configure(text="Invalid format! Use #RRGGBB", text_color="#FF4C4C")
        return
        
    try:
        preview_frame.configure(fg_color=hex_color)
        status_label.configure(text="Starting in 2 seconds... Release the mouse!", text_color="#F4D03F")
        app.update()
        time.sleep(2)
        
        status_label.configure(text="Syncing devices...", text_color="#3498DB")
        app.update()
        
        apply_color_to_all(hex_color)
        
        status_label.configure(text="Sync Completed Successfully!", text_color="#2ECC71")
        
    except Exception as e:
        status_label.configure(text="Error applying color or invalid Hex.", text_color="#FF4C4C")

# --- Main Window Setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

app = ctk.CTk()
app.geometry("450x380") 
app.title("RGB Sync Hub")
app.resizable(False, False)

# --- UI Elements ---
title_label = ctk.CTkLabel(app, text="Setup RGB Sync", font=("Segoe UI", 24, "bold"))
title_label.pack(pady=(20, 10))

instruction_label = ctk.CTkLabel(app, text="Enter Hex, use the eyedropper\nor click the color box to open spectrum:", font=("Segoe UI", 14))
instruction_label.pack(pady=(10, 5))

input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(pady=5)

color_input = ctk.CTkEntry(input_frame, width=120, font=("Segoe UI", 16), justify="center")
color_input.insert(0, "#FF00FF") 
color_input.pack(side="left", padx=(0, 10))

picker_button = ctk.CTkButton(input_frame, text="🎨 Pick", width=60, font=("Segoe UI", 14, "bold"),
                             fg_color="#34495E", hover_color="#2C3E50", command=open_color_picker)
picker_button.pack(side="left")

preview_frame = ctk.CTkFrame(app, width=100, height=40, fg_color="#FF00FF", corner_radius=8, cursor="hand2")
preview_frame.pack(pady=(10, 15))

preview_frame.bind("<Button-1>", open_color_spectrum)

sync_button = ctk.CTkButton(app, text="Sync Setup", font=("Segoe UI", 16, "bold"), 
                            height=40, command=start_automation)
sync_button.pack(pady=10)

status_label = ctk.CTkLabel(app, text="", font=("Segoe UI", 14, "bold"))
status_label.pack(pady=(5, 0))

# ==========================================
# 5. EXECUTION
# ==========================================
if __name__ == "__main__":
    app.mainloop()
