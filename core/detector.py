import mediapipe as mp
import cv2
import config
import math

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        # Start with the default from config
        self.setup_hands(config.MAX_HANDS)

    def setup_hands(self, max_hands):
        """Re-initializes the MediaPipe Hands object with a new max_hands limit."""
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            model_complexity=config.MODEL_COMPLEXITY,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )

    def set_max_hands(self, n):
        self.setup_hands(n)

    def find_hands(self, frame):
        # MediaPipe needs RGB, OpenCV uses BGR
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        return frame

    def get_hands_info(self, frame):
        hands_data = []
        if self.results.multi_hand_landmarks and self.results.multi_handedness:
            h, w, c = frame.shape
            for hand_lms, hand_info in zip(self.results.multi_hand_landmarks, self.results.multi_handedness):
                lm_list = []
                x_list, y_list = [], []
                for id, lm in enumerate(hand_lms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                    x_list.append(cx)
                    y_list.append(cy)

                label = hand_info.classification[0].label 
                hands_data.append({
                    'type': label,
                    'lm_list': lm_list,
                    'bbox': (min(x_list), min(y_list), max(x_list)-min(x_list), max(y_list)-min(y_list))
                })
        return hands_data
