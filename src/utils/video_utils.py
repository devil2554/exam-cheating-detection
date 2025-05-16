import cv2
import os
from datetime import datetime

class VideoRecorder:
    def __init__(self, config):
        self.recording_path = config['video']['recording_path']
        self.resolution = tuple(config['video']['resolution'])
        self.fps = config['video']['fps']
        self.writer = None
        self.current_file = None
        
    def start_recording(self):
        if not os.path.exists(self.recording_path):
            os.makedirs(self.recording_path)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_file = os.path.join(self.recording_path, f"session_{timestamp}.avi")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer = cv2.VideoWriter(self.current_file, fourcc, self.fps, self.resolution)
        
    def record_frame(self, frame):
        if self.writer is not None:
            self.writer.write(frame)
            
    def stop_recording(self):
        if self.writer is not None:
            self.writer.release()
            self.writer = None
            return self.current_file
        return None