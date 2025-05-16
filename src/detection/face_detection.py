import cv2
import torch
from facenet_pytorch import MTCNN
from datetime import datetime

class FaceDetector:
    def __init__(self, config):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.detector = MTCNN(
            keep_all=True,
            post_process=False,
            min_face_size=40,
            thresholds=[0.6, 0.7, 0.7],
            device=self.device
        )
        self.config = config
        self.detection_interval = config['detection']['face']['detection_interval']
        self.min_confidence = config['detection']['face']['min_confidence']
        self.frame_count = 0
        self.face_present = False
        self.last_face_time = None
        self.alert_logger = None
        self.face_disappeared_start = None

    def set_alert_logger(self, alert_logger):
        self.alert_logger = alert_logger

    def detect_face(self, frame):
        self.frame_count += 1
        if self.frame_count % self.detection_interval != 0:
            return self.face_present
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, probs = self.detector.detect(rgb_frame)
        
        current_time = datetime.now()
        if boxes is not None and len(boxes) > 0 and probs[0] > self.min_confidence:
            if not self.face_present and self.face_disappeared_start:
                disappearance_duration = (current_time - self.face_disappeared_start).total_seconds()
                if disappearance_duration > 5 and self.alert_logger:
                    self.alert_logger.log_alert(
                        "FACE_REAPPEARED",
                        f"Face reappeared after {disappearance_duration:.1f} seconds"
                    )
            
            self.face_present = True
            self.last_face_time = current_time
            self.face_disappeared_start = None
            return True
        else:
            if self.face_present:
                self.face_disappeared_start = current_time
                
            self.face_present = False
            if self.last_face_time and (current_time - self.last_face_time).total_seconds() > 5:
                if self.alert_logger:
                    self.alert_logger.log_alert(
                        "FACE_DISAPPEARED",
                        "Face disappeared for more than 5 seconds"
                    )
            return False