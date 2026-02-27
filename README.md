# Why are there two separate scripts?

Most proprietary hardware lighting software lacks public APIs for direct code integration. To bypass this limitation and instantly sync the RGB lighting across **three different hardware control apps** at the same time, this project relies on GUI Automation (simulating human mouse clicks).

However, screen resolutions and window placements vary from monitor to monitor. Hardcoding my specific screen coordinates would make the script useless for anyone else. 

To solve this, the project is divided into two parts:

1. **The Mapper (Radar):** A utility script that continuously prints the current X and Y coordinates of your mouse pointer. You use this first to map the exact click locations of the color buttons inside your three RGB apps.
2. **The Main Executor:** The actual `.exe` application. It takes the custom coordinates you mapped and uses `pyautogui` to instantly take over the mouse, open all three lighting programs, and click the correct colors across all of them in milliseconds.
