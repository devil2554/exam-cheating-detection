# import cv2
# import os
# from datetime import datetime

# class VideoRecorder:
#     def __init__(self, config):
#         self.recording_path = config['video']['recording_path']
#         self.resolution = tuple(config['video']['resolution'])
#         self.fps = config['video']['fps']
#         self.writer = None
#         self.current_file = None
        
#     def start_recording(self):
#         if not os.path.exists(self.recording_path):
#             os.makedirs(self.recording_path)
            
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         self.current_file = os.path.join(self.recording_path, f"session_{timestamp}.avi")
#         fourcc = cv2.VideoWriter_fourcc(*'XVID')
#         self.writer = cv2.VideoWriter(self.current_file, fourcc, self.fps, self.resolution)
        
#     def record_frame(self, frame):
#         if self.writer is not None:
#             self.writer.write(frame)
            
#     def stop_recording(self):
#         if self.writer is not None:
#             self.writer.release()
#             self.writer = None
#             return self.current_file
#         return None

import cv2
import os
from datetime import datetime

class VideoRecorder:
    def __init__(self, config):
        self.config = config['video']
        self.recording_path = config['video']['recording_path']
        self.resolution = tuple(config['video']['resolution'])
        self.fps = config['video']['fps']
        self.writer = None
        self.filename = None
        self.frame_count = 0
        self.start_time = datetime.now()
        
    def start_recording(self):
        if not os.path.exists(self.recording_path):
            os.makedirs(self.recording_path)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(self.recording_path, f"webcam_{timestamp}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(
            self.filename,
            fourcc,
            self.fps,
            self.resolution
        )
        
    def record_frame(self, frame):
        if self.writer:
            self.writer.write(frame)
            self.frame_count += 1
            
    def stop_recording(self):
        if self.writer:
            self.writer.release()
            self.writer = None
            duration = (datetime.now() - self.start_time).total_seconds()
            return {
                'filename': self.filename,
                'frame_count': self.frame_count,
                'duration': duration,
                'fps': self.frame_count / duration if duration > 0 else 0
            }
        return None