# import cv2
# import torch
# from ultralytics import YOLO
# from datetime import datetime

# class ObjectDetector:
#     def __init__(self, config):
#         self.config = config['detection']['objects']
#         self.model = None
#         self.class_map = {
#             73: 'book',
#             67: 'cell phone'
#         }
#         self.alert_logger = None
#         self.detection_interval = self.config['detection_interval']
#         self.frame_count = 0
#         self._initialize_model()

#     def _initialize_model(self):
#         """Safely initialize the YOLO model"""
#         try:
#             self.model = YOLO('models/yolov8n.pt')
#             # Warm up the model
#             dummy_input = torch.zeros((1, 3, 640, 640))
#             self.model(dummy_input)
#         except Exception as e:
#             raise RuntimeError(f"Failed to initialize object detector: {str(e)}")

#     def set_alert_logger(self, alert_logger):
#         self.alert_logger = alert_logger

#     def detect_objects(self, frame, visualize=False):
#         """Detect forbidden objects in frame"""
#         self.frame_count += 1
#         if self.frame_count % self.detection_interval != 0:
#             return False
            
#         try:
#             results = self.model(frame)
#             detected = False
            
#             for result in results:
#                 for box in result.boxes:
#                     cls = int(box.cls)
#                     conf = float(box.conf)
                    
#                     if cls in self.class_map and conf > self.config['min_confidence']:
#                         detected = True
#                         label = self.class_map[cls]
                        
#                         if self.alert_logger:
#                             self.alert_logger.log_alert(
#                                 "FORBIDDEN_OBJECT",
#                                 f"Detected {label} with confidence {conf:.2f}"
#                             )
                        
#                         if visualize:
#                             x1, y1, x2, y2 = map(int, box.xyxy[0])
#                             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
#                             cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10),
#                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
#             return detected
            
#         except Exception as e:
#             if self.alert_logger:
#                 self.alert_logger.log_alert(
#                     "OBJECT_DETECTION_ERROR",
#                     f"Object detection failed: {str(e)}"
#                 )
#             return False


import cv2
import torch
from ultralytics import YOLO
from datetime import datetime

class ObjectDetector:
    def __init__(self, config):
        self.config = config['detection']['objects']
        self.model = None
        self.class_map = {
            73: 'book',
            67: 'cell phone'
        }
        self.alert_logger = None
        self.detection_interval = self.config['detection_interval']
        self.frame_count = 0
        self._initialize_model()
        self.last_detection_time = datetime.now()

    def _initialize_model(self):
        """Initialize optimized YOLO model"""
        try:
            # Use the smallest YOLOv8 model for speed
            self.model = YOLO('models/yolov8n.pt')
            
            # Optimize model settings
            self.model.overrides['conf'] = self.config['min_confidence']
            self.model.overrides['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.model.overrides['imgsz'] = 320  # Smaller input size for faster processing
            # self.model.overrides['half'] = True  # Use FP16 precision if GPU available
            self.model.overrides['iou'] = 0.45   # Slightly higher IOU threshold

            
            # Warm up the model
            dummy_input = torch.zeros((1, 3, 320, 320)).to(self.model.device)
            self.model(dummy_input)
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize object detector: {str(e)}")

    def set_alert_logger(self, alert_logger):
        self.alert_logger = alert_logger

    def detect_objects(self, frame, visualize=False):
        """Optimized object detection with frame skipping"""
        current_time = datetime.now()
        time_since_last = (current_time - self.last_detection_time).total_seconds()
        
        # Skip detection if not enough time has passed
        if time_since_last < (1.0 / self.config['max_fps']):
            return False
            
        try:
            # Resize frame for faster processing (maintaining aspect ratio)
            orig_h, orig_w = frame.shape[:2]
            new_w = 320
            new_h = int(orig_h * (new_w / orig_w))
            resized_frame = cv2.resize(frame, (new_w, new_h))
            
            # Run inference
            results = self.model(resized_frame, verbose=False)  # Disable logging
            
            detected = False
            for result in results:
                for box in result.boxes:
                    cls = int(box.cls)
                    conf = float(box.conf)
                    
                    if cls in self.class_map and conf > self.config['min_confidence']:
                        detected = True
                        label = self.class_map[cls]
                        
                        if self.alert_logger:
                            self.alert_logger.log_alert(
                                "FORBIDDEN_OBJECT",
                                f"Detected {label} with confidence {conf:.2f}"
                            )
                        
                        if visualize:
                            # Scale coordinates back to original frame size
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1 = int(x1 * (orig_w / new_w))
                            y1 = int(y1 * (orig_h / new_h))
                            x2 = int(x2 * (orig_w / new_w))
                            y2 = int(y2 * (orig_h / new_h))
                            
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
            self.last_detection_time = current_time
            return detected
            
        except Exception as e:
            if self.alert_logger:
                self.alert_logger.log_alert(
                    "OBJECT_DETECTION_ERROR",
                    f"Object detection failed: {str(e)}"
                )
            return False