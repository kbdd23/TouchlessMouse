# TouchlessMouse Configuration

# Camera Settings
CAMERA_INDEX = 0          # Usually 0 is the built-in webcam
FRAME_WIDTH = 320         # MAX FPS MODE
FRAME_HEIGHT = 240
FPS_TARGET = 60

# Hand Detection
MIN_DETECTION_CONFIDENCE = 0.5 # Lowered for better detection in various lighting
MIN_TRACKING_CONFIDENCE = 0.6 # Lowered to keep the lock more easily
MAX_HANDS = 1             # Only track one hand for stability
MODEL_COMPLEXITY = 1      # 0 = Lite (Fastest), 1 = Full (Default). 1 improves accuracy significantly.

# Smoothing (Jitter Reduction)
SMOOTHING_FACTOR = 1      # Higher = Smoother but more lag (Try 2-3 for speed)

# Interaction Zones
PINKY_TRIGGER_RATIO = 0.5 # Separation required to ACTIVATE (Pinky Tip vs Ring Tip)
PINKY_RELEASE_RATIO = 0.3 # Separation required to DEACTIVATE (Hysteresis stability)
UNFREEZE_DELAY = 0.5      # Seconds to keep cursor frozen after pinky retracts (Stabilizer)
DRAG_ACTIVATION_TIME = 2.0 # Seconds to hold Middle Finger to trigger Drag/Scroll
SCREEN_MARGIN = 0       # Dead zone around the camera frame edges
SENSITIVITY = 25.0        # High sensitivity for low-res input (Speed Match)
SENSITIVITY_PRECISION = 7.5 # Precision Mode (Slow/Sniper) when Pinky is out

# Debug
SHOW_DEBUG_WINDOW = True
DISPLAY_WIDTH = 600       # Size of the debug window on screen
DISPLAY_HEIGHT = 400
DRAW_LANDMARKS = True
