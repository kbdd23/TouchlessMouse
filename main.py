import cv2
import time
import config
from core.camera import CameraStream
from core.detector import HandDetector
from core.interpreter import GestureInterpreter
from core.controller import CursorController
from utils.smoothing import ExponentialSmoothing

def main():
    # Initialize Modules
    camera = CameraStream().start() 
    detector = HandDetector()
    interpreter = GestureInterpreter()
    controller = CursorController()
    smoother = ExponentialSmoothing(alpha=config.SMOOTHING_FACTOR)

    p_time = 0
    prev_x, prev_y = None, None 
    last_lock_state = None # To detect transitions
    
    if config.SHOW_DEBUG_WINDOW:
        window_name = "Touchless Mouse Debug"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
    
    print("Touchless Mouse Started. Press 'q' to exit.")

    try:
        while True:
            frame = camera.read()
            if frame is None: continue 

            # 1. Detect transition to Optimize Performance
            current_lock = interpreter.locked_hand_type
            if current_lock != last_lock_state:
                if current_lock is None:
                    detector.set_max_hands(2) # Search Mode
                else:
                    detector.set_max_hands(1) # Performance Mode (Only 1 hand tracked)
                last_lock_state = current_lock

            # 2. Get Hands Data
            frame = detector.find_hands(frame)
            hands_data = detector.get_hands_info(frame)

            # 3. Process Hands
            action, coords, visual_list, extra_feedback = interpreter.process_hands(hands_data)
            
            # --- EXECUTE ACTION (PRIORITY) ---
            if action != "NONE" and action != "STOP":
                x_raw, y_raw = coords
                x_smooth, y_smooth = smoother.smooth(x_raw, y_raw)

                if action in ["MOVE", "DRAG", "PRECISION", "DRAG_PRECISION"]:
                    if prev_x is None:
                        prev_x, prev_y = x_smooth, y_smooth
                    else:
                        dx = x_smooth - prev_x
                        dy = y_smooth - prev_y
                        sens = config.SENSITIVITY_PRECISION if "PRECISION" in action else config.SENSITIVITY
                        if "DRAG" in action: controller.start_drag()
                        controller.move_relative(dx * sens, dy * sens)
                        prev_x, prev_y = x_smooth, y_smooth
                elif action == "CLICK":
                    controller.click()
                    prev_x, prev_y = x_smooth, y_smooth
                elif action == "RIGHT_CLICK":
                    controller.right_click()
                    prev_x, prev_y = x_smooth, y_smooth
                elif action == "DROP":
                    controller.stop_drag()
                    prev_x, prev_y = x_smooth, y_smooth
                elif action == "FREEZE":
                    prev_x, prev_y = x_smooth, y_smooth
            else:
                prev_x, prev_y = None, None

            # --- VISUAL FEEDBACK (OPTIONAL) ---
            if config.SHOW_DEBUG_WINDOW:
                # Global Feedback (Small White Circle)
                for fb_type, fb_coords in extra_feedback:
                    if fb_type == 'CIRCLE_WHITE':
                        cv2.circle(frame, (int(fb_coords[0]), int(fb_coords[1])), 8, (255, 255, 255), cv2.FILLED)
                        cv2.circle(frame, (int(fb_coords[0]), int(fb_coords[1])), 10, (0, 0, 0), 2)

                # Active Hand Feedback
                if interpreter.locked_hand_type:
                    active_hand = next((h for h in hands_data if h['type'] == interpreter.locked_hand_type), None)
                    if active_hand:
                        lm_list = active_hand['lm_list']
                        # Index (Green)
                        cv2.circle(frame, (lm_list[8][1], lm_list[8][2]), 8, (0, 255, 0), cv2.FILLED)
                        # Gestures
                        for v_state, v_id in visual_list:
                            color = (0, 165, 255) if v_state == 1 else (255, 255, 0) # Orange vs Cyan
                            if v_state == 3: # STOP
                                for fid in [8, 12, 16, 20]: cv2.circle(frame, (lm_list[fid][1], lm_list[fid][2]), 8, (0, 0, 255), cv2.FILLED)
                            elif v_state == 4: # Sniper
                                cv2.circle(frame, (lm_list[v_id][1], lm_list[v_id][2]), 8, (0, 0, 255), cv2.FILLED)
                            elif v_state > 0:
                                cv2.circle(frame, (lm_list[v_id][1], lm_list[v_id][2]), 8, color, cv2.FILLED)
                        # Action Pops
                        if action == "CLICK": cv2.circle(frame, coords, 8, (0, 255, 0), cv2.FILLED)
                        elif action == "RIGHT_CLICK": cv2.circle(frame, coords, 12, (255, 255, 0), cv2.FILLED)

                # FPS (Minimal)
                c_time = time.time()
                fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
                p_time = c_time
                cv2.putText(frame, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

                cv2.imshow(window_name, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'): break
    
    except KeyboardInterrupt: print("Stopping...")
    finally:
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__": main()