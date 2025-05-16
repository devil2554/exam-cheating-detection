import cv2
import mediapipe as mp
import numpy as np

class MouthMonitor:
    def __init__(self, config):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
            
        self.mouth_threshold = config['detection']['mouth']['movement_threshold']
        self.mouth_movement_count = 0
        self.last_mouth_time = None
        self.alert_logger = None  # Will be set externally
        
    def set_alert_logger(self, alert_logger):
        self.alert_logger = alert_logger
        
    def monitor_mouth(self, frame):
        results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if not results.multi_face_landmarks:
            return False
            
        face_landmarks = results.multi_face_landmarks[0]
        
        # Get mouth landmarks (using more points for better accuracy)
        mouth_points = [
            13,  # Upper inner lip
            14,  # Lower inner lip
            78,  # Right corner
            306,  # Left corner
            312,  # Upper outer lip
            317,  # Lower outer lip
        ]
        
        # Calculate mouth openness
        upper_lip = face_landmarks.landmark[13].y
        lower_lip = face_landmarks.landmark[14].y
        mouth_open = lower_lip - upper_lip
        
        # Calculate mouth width
        right_corner = face_landmarks.landmark[78].x
        left_corner = face_landmarks.landmark[306].x
        mouth_width = abs(right_corner - left_corner)
        
        if mouth_open > 0.03 or mouth_width > 0.2:  # Thresholds for mouth movement
            self.mouth_movement_count += 1
            
            if self.mouth_movement_count > self.mouth_threshold and self.alert_logger:
                self.alert_logger.log_alert(
                    "MOUTH_MOVEMENT", 
                    "Excessive mouth movement detected (possible talking)"
                )
                self.mouth_movement_count = 0
            return True
        else:
            self.mouth_movement_count = max(0, self.mouth_movement_count - 1)
            return False