import math
import time
import config

class GestureInterpreter:
    def __init__(self):
        self.last_pinky_time = 0
        self.is_extended_prev = False
        self.double_tap_timeout = 0.4 
        self.pinky_release_time = 0
        self.pinky_active = False # State for Hysteresis Filter
        
        # Drag / Middle Finger State
        self.middle_finger_start_time = 0
        self.is_dragging = False

    def get_gesture(self, lm_list):
        if len(lm_list) < 21:
            return "NONE", None, 0

        # Helper to check which fingers are up
        fingers = []
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]

        for i in range(4):
            if lm_list[tip_ids[i]][2] < lm_list[pip_ids[i]][2]:
                fingers.append(True)
            else:
                fingers.append(False)

        index_up = fingers[0]
        middle_up = fingers[1]
        ring_up = fingers[2]

        # Coordinates
        x_index, y_index = lm_list[8][1], lm_list[8][2]   # Index Tip
        x_pinky, y_pinky = lm_list[20][1], lm_list[20][2] # Pinky Tip
        x_ring, y_ring = lm_list[16][1], lm_list[16][2]   # Ring Tip
        
        # --- PINKY LOGIC (SNIPER MODE) ---
        # Check Pinky "Separation" State (Hysteresis)
        x_wrist, y_wrist = lm_list[0][1], lm_list[0][2]
        x_mid_mcp, y_mid_mcp = lm_list[9][1], lm_list[9][2]
        palm_size = math.hypot(x_wrist - x_mid_mcp, y_wrist - y_mid_mcp)
        if palm_size == 0: palm_size = 1

        separation = math.hypot(x_pinky - x_ring, y_pinky - y_ring)
        ratio = separation / palm_size
        
        if not self.pinky_active:
            if ratio > config.PINKY_TRIGGER_RATIO: self.pinky_active = True
        else:
            if ratio < config.PINKY_RELEASE_RATIO: self.pinky_active = False
        
        is_sniper = self.pinky_active
        
        # --- MIDDLE FINGER LOGIC (DRAG / SCROLL) ---
        drag_state = 0 # 0: None, 1: Charging, 2: Active
        
        # STRICT POSTURE CHECK:
        # Index must be UP, Middle must be UP, AND Ring must be DOWN (prevents charging on Open Hand)
        if index_up and middle_up and not ring_up: 
            if self.middle_finger_start_time == 0:
                self.middle_finger_start_time = time.time()
            
            elapsed = time.time() - self.middle_finger_start_time
            
            if elapsed > config.DRAG_ACTIVATION_TIME:
                self.is_dragging = True
                drag_state = 2 # Active
            else:
                drag_state = 1 # Charging
        else:
            # Posture broken or Middle finger dropped
            self.middle_finger_start_time = 0
            if self.is_dragging:
                self.is_dragging = False
                return "DROP", (x_index, y_index), 0

        # --- COMBINED ACTION LOGIC ---
        
        # If we are dragging, the action is always DRAG (or DRAG_PRECISION)
        if self.is_dragging:
            if is_sniper:
                return "DRAG_PRECISION", (x_index, y_index), drag_state
            else:
                return "DRAG", (x_index, y_index), drag_state

        # Normal Pointer Logic (Index Up, Ring Down)
        # We ignore middle_up check here because we handled it above (it's either charging or not)
        if index_up and not ring_up:
            
            # If we are CHARGING drag (middle up < 2s), we still move normally
            # Visualization will handle the yellow dot
            
            if is_sniper:
                # SNIPER MODE
                self.pinky_release_time = time.time()
                action = "PRECISION" 
                
                if not self.is_extended_prev: # Rising Edge of Pinky
                    current_time = time.time()
                    dt = current_time - self.last_pinky_time
                    
                    if dt < self.double_tap_timeout:
                        action = "CLICK"
                        self.last_pinky_time = 0 
                    else:
                        self.last_pinky_time = current_time
                
                self.is_extended_prev = True
                return action, (x_index, y_index), drag_state
            
            else:
                # NORMAL MOVE
                self.is_extended_prev = False
                
                if time.time() - self.pinky_release_time < config.UNFREEZE_DELAY:
                    return "FREEZE", (x_index, y_index), drag_state
                
                return "MOVE", (x_index, y_index), drag_state

        return "NONE", None, 0
