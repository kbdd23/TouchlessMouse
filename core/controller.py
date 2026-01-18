import pyautogui
import numpy as np
import config

class CursorController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()
        pyautogui.FAILSAFE = False # Allow reaching corners without crashing
        pyautogui.PAUSE = 0       # CRITICAL: Remove 0.1s delay for smooth real-time control

    def move(self, x, y):
        # Absolute movement (Legacy/Fallback)
        # Convert Camera Coordinates to Screen Coordinates with Margins
        x = np.clip(x, config.SCREEN_MARGIN, config.FRAME_WIDTH - config.SCREEN_MARGIN)
        y = np.clip(y, config.SCREEN_MARGIN, config.FRAME_HEIGHT - config.SCREEN_MARGIN)
        screen_x = np.interp(x, (config.SCREEN_MARGIN, config.FRAME_WIDTH - config.SCREEN_MARGIN), (0, self.screen_w))
        screen_y = np.interp(y, (config.SCREEN_MARGIN, config.FRAME_HEIGHT - config.SCREEN_MARGIN), (0, self.screen_h))
        pyautogui.moveTo(screen_x, screen_y)

    def move_relative(self, dx, dy):
        # Relative movement (Trackpad style)
        # Sensitivity is now applied externally (in main.py) to support different modes (Normal vs Precision)
        
        # PyAutoGUI handles float inputs gracefully, but let's be safe
        pyautogui.move(dx, dy)

    def click(self):
        pyautogui.click()

    def start_drag(self):
        pyautogui.mouseDown()

    def stop_drag(self):
        pyautogui.mouseUp()
