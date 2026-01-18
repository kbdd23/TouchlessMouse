import numpy as np

class ExponentialSmoothing:
    def __init__(self, alpha=2):
        self.base_alpha = alpha # Config value (e.g., 2)
        self.prev_x = 0.0
        self.prev_y = 0.0

    def smooth(self, curr_x, curr_y):
        # Initialize
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x, self.prev_y = float(curr_x), float(curr_y)
            return curr_x, curr_y

        # Calculate Movement Magnitude (Manhattan distance is faster than sqrt)
        # How much did the raw input change?
        dx = curr_x - self.prev_x
        dy = curr_y - self.prev_y
        dist = abs(dx) + abs(dy)

        # ADAPTIVE LOGIC
        # 1. Fast Movement (Flick): Low smoothing for instant response
        if dist > 30: 
            active_alpha = self.base_alpha # e.g. 2 (Fast)
        
        # 2. Jitter Zone (Still/Micro): High smoothing to kill tremble
        elif dist < 5:
            active_alpha = self.base_alpha * 4 # e.g. 8 (Rock Solid)
            
        # 3. Normal Movement: Medium smoothing
        else:
            active_alpha = self.base_alpha * 2 # e.g. 4 (Balanced)

        # Apply Exponential Smoothing
        # Formula: New = Old + (Target - Old) / Factor
        smooth_x = self.prev_x + (curr_x - self.prev_x) / active_alpha
        smooth_y = self.prev_y + (curr_y - self.prev_y) / active_alpha

        self.prev_x, self.prev_y = smooth_x, smooth_y
        
        return int(smooth_x), int(smooth_y)