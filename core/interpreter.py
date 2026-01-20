import math
import time
import config

class GestureInterpreter:
    def __init__(self):
        # --- HAND LOCKING STATE ---
        self.locked_hand_type = None # None, 'Left', 'Right'
        
        # Dictionary to track Fist history independently for Left and Right hands
        # Format: {'Left': False, 'Right': False}
        self.fist_history = {} 
        
        # --- GESTURE STATES ---
        self.last_pinky_time = 0
        self.is_extended_prev = False
        self.double_tap_timeout = 0.4 
        self.pinky_release_time = 0
        self.pinky_active = False # State for Hysteresis Filter
        
        # Drag / Middle Finger State
        self.middle_finger_start_time = 0
        self.is_dragging = False

        # Right Click State
        self.rc_start_time = 0
        self.rc_triggered = False
        self.rc_needs_reset = False

    def is_fist(self, lm_list):
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        closed_count = 0
        for i in range(4):
            if lm_list[tips[i]][2] > lm_list[pips[i]][2]: # Tip below PIP = Closed
                closed_count += 1
        return closed_count == 4

    def is_open_hand(self, lm_list):
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        open_count = 0
        for i in range(4):
            if lm_list[tips[i]][2] < lm_list[pips[i]][2]: # Tip above PIP = Open
                open_count += 1
        return open_count == 4

    def process_hands(self, hands_data):
        # Wrapper to handle locking logic before processing gestures
        # Returns: Action, Coords, VisualList, HandToDraw(bbox/info)
        
        target_hand = None
        visual_feedback = [] # Global visual feedback (like the white circle)
        
        # --- STEP 1: IDENTIFY TARGET HAND ---
        
        if self.locked_hand_type is None:
            # IDLE MODE: Look for ANY hand making a transition FIST -> OPEN
            
            # Temporary dict to track current frame state to update history later if needed
            # Actually, we update history live.
            
            for hand in hands_data:
                label = hand['type']
                lm_list = hand['lm_list']
                
                # Check posture
                is_fist_now = self.is_fist(lm_list)
                is_open_now = self.is_open_hand(lm_list)
                
                was_fist_before = self.fist_history.get(label, False)

                if is_fist_now:
                    # Found a fist! Show feedback (White Circle on Wrist)
                    wrist = lm_list[0]
                    visual_feedback.append(('CIRCLE_WHITE', (wrist[1], wrist[2])))
                    
                    # Update History: This hand IS a fist right now.
                    self.fist_history[label] = True
                
                elif is_open_now:
                    # If this SPECIFIC hand was a fist just before... LOCK IT!
                    if was_fist_before:
                        # LOCK DETECTED
                        self.locked_hand_type = label
                        self.fist_history = {} # Clear history
                        target_hand = hand
                        break # Stop looking, we found our partner
                    else:
                        # Just an open hand without prior fist. 
                        self.fist_history[label] = False
                else:
                    # Neither Fist nor Full Open (maybe transition or random)
                    # Reset history to be safe/strict? 
                    # Or keep it True to allow a few transition frames?
                    # Strict is better to avoid false positives.
                    self.fist_history[label] = False
        
        else:
            # LOCKED MODE: Only look for the specific hand
            found = False
            for hand in hands_data:
                if hand['type'] == self.locked_hand_type:
                    target_hand = hand
                    found = True
                    break
            
            if not found:
                pass
            else:
                # Check for UNLOCK Gesture (Fist)
                if self.is_fist(target_hand['lm_list']):
                    # UNLOCKED
                    self.locked_hand_type = None
                    target_hand = None 
                    self.fist_history = {} # Reset
                    
                    # Show white circle feedback
                    wrist = hand['lm_list'][0]
                    visual_feedback.append(('CIRCLE_WHITE', (wrist[1], wrist[2])))

        # --- STEP 2: PROCESS GESTURES ON TARGET HAND ---
        if target_hand:
            action, coords, v_list = self.get_gesture(target_hand['lm_list'])
            return action, coords, v_list, visual_feedback
        else:
            return "NONE", None, [], visual_feedback

    def get_gesture(self, lm_list):
        visual_states = []
        if len(lm_list) < 21: return "NONE", None, []

        fingers = []
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]

        for i in range(4):
            if lm_list[tip_ids[i]][2] < lm_list[pip_ids[i]][2]:
                fingers.append(True)
            else:
                fingers.append(False)

        index_up, middle_up, ring_up, pinky_up = fingers

        # Thumb Detection
        x_tip, x_ip = lm_list[4][1], lm_list[3][1]
        x_center = lm_list[9][1]
        dist_tip_center = abs(x_tip - x_center)
        dist_ip_center = abs(x_ip - x_center)
        thumb_up = dist_tip_center > (dist_ip_center * config.STOP_THUMB_SENSITIVITY)

        x_index, y_index = lm_list[8][1], lm_list[8][2]
        x_pinky, y_pinky = lm_list[20][1], lm_list[20][2]
        x_ring, y_ring = lm_list[16][1], lm_list[16][2]
        
        # STOP Logic (5 Fingers)
        if index_up and middle_up and ring_up and pinky_up and thumb_up:
            self.middle_finger_start_time = 0
            self.is_dragging = False
            self.rc_start_time = 0
            self.rc_triggered = False
            self.rc_needs_reset = False
            visual_states.append((3, 0)) 
            return "STOP", (x_index, y_index), visual_states

        # Anatomical Assist
        if pinky_up and not ring_up:
             if lm_list[16][2] < lm_list[13][2]: ring_up = True

        # Pinky Logic
        if ring_up:
            self.pinky_active = pinky_up
        else:
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
        
        # Add visual feedback for Pinky (Sniper Mode)
        if is_sniper:
            visual_states.append((4, 20)) 
        
        # Right Click Logic
        if index_up and ring_up:
            self.middle_finger_start_time = 0
            self.is_dragging = False
            if self.rc_needs_reset:
                visual_states.append((2, 16))
                if middle_up: visual_states.append((2, 12))
            else:
                if self.rc_start_time == 0: self.rc_start_time = time.time()
                elapsed = time.time() - self.rc_start_time
                if elapsed > config.RIGHT_CLICK_DELAY:
                    self.rc_triggered = True
                    self.rc_needs_reset = True
                    visual_states.append((2, 16))
                    if middle_up: visual_states.append((2, 12))
                    return "RIGHT_CLICK", (x_index, y_index), visual_states
                else:
                    visual_states.append((1, 16))
                    if middle_up: visual_states.append((1, 12))
        else:
            self.rc_start_time = 0
            self.rc_needs_reset = False
            self.rc_triggered = False

            # Drag Logic
            drag_state_val = 0
            if index_up and middle_up and not ring_up: 
                if self.middle_finger_start_time == 0: self.middle_finger_start_time = time.time()
                elapsed = time.time() - self.middle_finger_start_time
                if elapsed > config.DRAG_ACTIVATION_TIME:
                    self.is_dragging = True
                    drag_state_val = 2 
                else:
                    drag_state_val = 1 
            else:
                self.middle_finger_start_time = 0
                if self.is_dragging:
                    self.is_dragging = False
                    return "DROP", (x_index, y_index), []
            if drag_state_val > 0:
                 visual_states.append((drag_state_val, 12))

        # Combined Action
        if self.is_dragging:
            if is_sniper: return "DRAG_PRECISION", (x_index, y_index), visual_states
            else: return "DRAG", (x_index, y_index), visual_states

        if index_up:
            if is_sniper:
                self.pinky_release_time = time.time()
                action = "PRECISION" 
                if not self.is_extended_prev:
                    current_time = time.time()
                    dt = current_time - self.last_pinky_time
                    if dt < self.double_tap_timeout:
                        action = "CLICK"
                        self.last_pinky_time = 0 
                    else:
                        self.last_pinky_time = current_time
                self.is_extended_prev = True
                return action, (x_index, y_index), visual_states
            else:
                self.is_extended_prev = False
                if time.time() - self.pinky_release_time < config.UNFREEZE_DELAY:
                    return "FREEZE", (x_index, y_index), visual_states
                return "MOVE", (x_index, y_index), visual_states

        return "NONE", None, visual_states
