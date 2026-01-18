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
    # Threaded Camera for Performance
    camera = CameraStream().start() 
    detector = HandDetector()
    interpreter = GestureInterpreter()
    controller = CursorController()
    smoother = ExponentialSmoothing(alpha=config.SMOOTHING_FACTOR)

    p_time = 0
    prev_x, prev_y = None, None # For relative movement tracking
    
    # Setup Window for GPU Scaling (No CPU cost)
    if config.SHOW_DEBUG_WINDOW:
        window_name = "Touchless Mouse Debug"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
    
    print("Touchless Mouse Started. Press 'q' to exit.")

    try:
        while True:
            frame = camera.read()
            if frame is None:
                continue # Wait for camera thread to warm up

            # 1. Find Hand Landmarks
            frame = detector.find_hands(frame)
            lm_list = detector.get_position(frame)

            if len(lm_list) != 0:
                # 2. Interpret Gesture
                # Returns: Action String, (x, y), Drag State (0, 1, 2)
                action, coords, drag_state = interpreter.get_gesture(lm_list)
                
                # --- VISUAL FEEDBACK FOR DRAG STATE ---
                # Drag State: 1 = Charging (Orange), 2 = Active (Cyan)
                if drag_state > 0:
                    # Get Middle Finger Tip (Landmark 12)
                    # format: [id, x, y]
                    mid_x, mid_y = lm_list[12][1], lm_list[12][2]
                    
                    if drag_state == 1:
                        # Charging: Orange (BGR: 0, 165, 255)
                        cv2.circle(frame, (mid_x, mid_y), 10, (0, 165, 255), cv2.FILLED)
                    elif drag_state == 2:
                        # Active: Cyan (BGR: 255, 255, 0)
                        cv2.circle(frame, (mid_x, mid_y), 12, (255, 255, 0), cv2.FILLED)

                if action != "NONE":
                    x_raw, y_raw = coords
                    
                    # 3. Smooth Coordinates
                    x_smooth, y_smooth = smoother.smooth(x_raw, y_raw)

                    # 4. Execute Action
                    if action == "MOVE" or action == "DRAG":
                        if prev_x is None:
                            prev_x, prev_y = x_smooth, y_smooth
                        else:
                            dx = x_smooth - prev_x
                            dy = y_smooth - prev_y
                            
                            # If DRAG, ensure mouse is held down
                            if action == "DRAG":
                                controller.start_drag()
                            
                            controller.move_relative(dx * config.SENSITIVITY, dy * config.SENSITIVITY)
                            prev_x, prev_y = x_smooth, y_smooth

                    elif action == "PRECISION" or action == "DRAG_PRECISION":
                        if prev_x is None:
                            prev_x, prev_y = x_smooth, y_smooth
                        else:
                            dx = x_smooth - prev_x
                            dy = y_smooth - prev_y
                            
                            if action == "DRAG_PRECISION":
                                controller.start_drag()
                            
                            controller.move_relative(dx * config.SENSITIVITY_PRECISION, dy * config.SENSITIVITY_PRECISION)
                            prev_x, prev_y = x_smooth, y_smooth

                    elif action == "FREEZE":
                        prev_x, prev_y = x_smooth, y_smooth

                    elif action == "CLICK":
                        cv2.circle(frame, (x_raw, y_raw), 15, (0, 255, 0), cv2.FILLED)
                        controller.click()
                        prev_x, prev_y = x_smooth, y_smooth
                    
                    elif action == "DROP":
                        # Release the drag
                        controller.stop_drag()
                        prev_x, prev_y = x_smooth, y_smooth

                else:
                    prev_x, prev_y = None, None
            else:
                 prev_x, prev_y = None, None

            # FPS Display
            c_time = time.time()
            fps = 1 / (c_time - p_time)
            p_time = c_time
            cv2.putText(frame, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            # Show Debug Window
            if config.SHOW_DEBUG_WINDOW:
                # No resize needed here! GPU handles window scaling via WINDOW_NORMAL
                cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
