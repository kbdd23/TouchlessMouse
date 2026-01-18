import mediapipe as mp
import cv2
import config
import math

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=config.MAX_HANDS,
            model_complexity=config.MODEL_COMPLEXITY,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )

    def find_hands(self, frame):
        # 1. Fast Lighting Normalization (Min-Max scaling)
        # This improves contrast without the heavy cost of CLAHE
        frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)

        # 2. MediaPipe needs RGB, OpenCV uses BGR
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if config.DRAW_LANDMARKS:
                    h, w, c = frame.shape
                    lms = hand_lms.landmark
                    
                    # 1. Index Tip (Cursor) - Green
                    idx_x, idx_y = int(lms[8].x * w), int(lms[8].y * h)
                    cv2.circle(frame, (idx_x, idx_y), 8, (0, 255, 0), cv2.FILLED)

                    # 2. Pinky Separation Logic (Movement Detection)
                    # Instead of length, we check separation between Pinky Tip (20) and Ring Tip (16)
                    pnk_x, pnk_y = int(lms[20].x * w), int(lms[20].y * h)
                    rng_x, rng_y = int(lms[16].x * w), int(lms[16].y * h)
                    
                    # Scale Reference (Wrist to Middle MCP)
                    wri_x, wri_y = int(lms[0].x * w), int(lms[0].y * h)
                    mid_x, mid_y = int(lms[9].x * w), int(lms[9].y * h)

                    # Calculate Distances
                    separation = math.hypot(pnk_x - rng_x, pnk_y - rng_y)
                    palm_size = math.hypot(wri_x - mid_x, wri_y - mid_y)
                    
                    # Safe Division
                    if palm_size == 0: palm_size = 1
                    ratio = separation / palm_size

                    # VISUAL DEBUG: Show the ratio so user understands detection
                    cv2.putText(frame, f"R: {ratio:.2f}", (pnk_x + 20, pnk_y), 
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)

                    # Draw Red Circle if Triggered
                    if ratio > config.PINKY_TRIGGER_RATIO: 
                        cv2.circle(frame, (pnk_x, pnk_y), 8, (0, 0, 255), cv2.FILLED)

        return frame

    def get_position(self, frame):
        lm_list = []
        if hasattr(self, 'results') and self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0]
            h, w, c = frame.shape
            for id, lm in enumerate(my_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list