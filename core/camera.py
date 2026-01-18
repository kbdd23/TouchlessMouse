import cv2
import config
from threading import Thread
import time

class CameraStream:
    def __init__(self):
        self.stream = cv2.VideoCapture(config.CAMERA_INDEX)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        # Try to force 30 FPS on hardware level
        self.stream.set(cv2.CAP_PROP_FPS, config.FPS_TARGET)
        
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        # Start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # Keep looping infinitely until the thread is stopped
        while True:
            if self.stopped:
                return
            
            (grabbed, frame) = self.stream.read()
            if grabbed:
                self.grabbed = grabbed
                self.frame = frame
            else:
                self.stopped = True

    def read(self):
        # Return the most recent frame
        if self.frame is not None:
             # Flip logic happens here so the main thread gets the correct view
            return cv2.flip(self.frame, 1)
        return None

    def release(self):
        self.stopped = True
        # Give thread time to stop
        time.sleep(0.1)
        self.stream.release()