# import cv2
# import yaml
# import time
# import torch
# from detection.face_detection import FaceDetector
# from detection.eye_tracking import EyeTracker
# from detection.mouth_detection import MouthMonitor
# from detection.multi_face import MultiFaceDetector
# from utils.video_utils import VideoRecorder
# from utils.logging import AlertLogger

# def load_config():
#     with open('config/config.yaml') as f:
#         return yaml.safe_load(f)

# def main():
#     config = load_config()
#     # print(config)
#     # Check for GPU availability
#     device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
#     print(f"Using device: {device}")
    
#     # Initialize components with device information
#     face_detector = FaceDetector(config)
#     eye_tracker = EyeTracker(config)
#     mouth_monitor = MouthMonitor(config)
#     multi_face_detector = MultiFaceDetector(config)
#     video_recorder = VideoRecorder(config)
#     alert_logger = AlertLogger(config)
    
#     # Start video capture
#     cap = cv2.VideoCapture(config['video']['source'])
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['video']['resolution'][0])
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['video']['resolution'][1])
    
#     video_recorder.start_recording()
    
#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
                
#             # Perform detections
#             face_present = face_detector.detect_face(frame)
#             gaze_direction = eye_tracker.track_eyes(frame)
#             mouth_moving = mouth_monitor.monitor_mouth(frame)
#             multiple_faces = multi_face_detector.detect_multiple_faces(frame)
            
#             # Record frame
#             video_recorder.record_frame(frame)
            
#             # Display results
#             cv2.imshow('Exam Monitoring', frame)
            
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
                
#     finally:
#         cap.release()
#         video_recorder.stop_recording()
#         cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()


# import cv2
# import yaml
# import time
# import torch
# from detection.face_detection import FaceDetector
# from detection.eye_tracking import EyeTracker
# from detection.mouth_detection import MouthMonitor
# from detection.multi_face import MultiFaceDetector
# from detection.object_detection import ObjectDetector
# from utils.video_utils import VideoRecorder
# from utils.logging import AlertLogger

# def load_config():
#     with open('config/config.yaml') as f:
#         return yaml.safe_load(f)

# def main():
#     config = load_config()
    
#     # Initialize alert logger first
#     alert_logger = AlertLogger(config)
    
#     # Initialize components
#     face_detector = FaceDetector(config)
#     eye_tracker = EyeTracker(config)
#     mouth_monitor = MouthMonitor(config)
#     multi_face_detector = MultiFaceDetector(config)
#     object_detector = ObjectDetector(config)
#     video_recorder = VideoRecorder(config)
    
#     # Set alert logger for all detection modules
#     face_detector.set_alert_logger(alert_logger)
#     eye_tracker.set_alert_logger(alert_logger)
#     mouth_monitor.set_alert_logger(alert_logger)
#     multi_face_detector.set_alert_logger(alert_logger)
#     object_detector.set_alert_logger(alert_logger)
    
#     # Start video capture
#     cap = cv2.VideoCapture(config['video']['source'])
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['video']['resolution'][0])
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['video']['resolution'][1])
    
#     video_recorder.start_recording()
    
#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
                
#             # Perform detections with error handling
#             try:
#                 face_present = face_detector.detect_face(frame)
#                 gaze_direction, eye_ratio = eye_tracker.track_eyes(frame)
#                 mouth_moving = mouth_monitor.monitor_mouth(frame)
#                 multiple_faces = multi_face_detector.detect_multiple_faces(frame)
#                 # object_detector = object_detector.detect_objects(frame, visualize=True)
                
#                 # Display information on frame
#                 cv2.putText(frame, f"Face: {'Present' if face_present else 'Absent'}", (10, 30),
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#                 # cv2.putText(frame, f"Gaze: {gaze_direction}", (10, 60),
#                 #            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#                 # cv2.putText(frame, f"Eye Ratio: {eye_ratio:.2f}", (10, 90),
#                 #            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#                 if gaze_direction == "left":
#                     cv2.putText(frame, "Looking LEFT", (frame.shape[1] - 200, 30),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                 elif gaze_direction == "right":
#                     cv2.putText(frame, "Looking RIGHT", (frame.shape[1] - 200, 30),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                 else:
#                     cv2.putText(frame, "Looking CENTER", (frame.shape[1] - 200, 30),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#                 eye_status = "Closed" if eye_ratio > eye_tracker.EYE_ASPECT_RATIO_THRESH else "Open"
#                 cv2.putText(frame, f"Eyes: {eye_status} ({eye_ratio:.2f})", (frame.shape[1] - 200, 60),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#                 cv2.putText(frame, f"Mouth: {'Moving' if mouth_moving else 'Still'}", (10, 120),
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#                 if multiple_faces:
#                     cv2.putText(frame, "Multiple Faces Detected!", (10, 150),
#                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                 if object_detector:
#                     cv2.putText(frame, "FORBIDDEN OBJECT DETECTED!", (10, 180),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
#                 # Record frame
#                 video_recorder.record_frame(frame)
                
#             except Exception as e:
#                 alert_logger.log_alert(
#                     "DETECTION_ERROR",
#                     f"Error in detection pipeline: {str(e)}"
#                 )
#                 continue
            
#             # Display results
#             cv2.imshow('Exam Monitoring', frame)
            
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
                
#     finally:
#         cap.release()
#         video_recorder.stop_recording()
#         cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()


import cv2
import yaml
from detection.face_detection import FaceDetector
from detection.eye_tracking import EyeTracker
from detection.mouth_detection import MouthMonitor
from detection.object_detection import ObjectDetector
from detection.multi_face import MultiFaceDetector
from utils.video_utils import VideoRecorder
from utils.logging import AlertLogger

def load_config():
    with open('config/config.yaml') as f:
        return yaml.safe_load(f)

def display_detection_results(frame, face_present, gaze_direction, eye_ratio, 
                            mouth_moving, multiple_faces, objects_detected):
    """Display all detection results on frame"""
    # Face status
    cv2.putText(frame, f"Face: {'Present' if face_present else 'Absent'}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Eye information
    eye_status = "Open" if eye_ratio > 0.25 else "Closed"
    cv2.putText(frame, f"Gaze: {gaze_direction}", (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Eyes: {eye_status}", (10, 90),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Mouth status
    cv2.putText(frame, f"Mouth: {'Moving' if mouth_moving else 'Still'}", (10, 120),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Multiple faces warning
    if multiple_faces:
        cv2.putText(frame, "Multiple Faces!", (10, 150),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Objects detected warning
    if objects_detected:
        cv2.putText(frame, "Forbidden Object!", (10, 180),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

def main():
    config = load_config()
    
    # Initialize components
    alert_logger = AlertLogger(config)
    video_recorder = VideoRecorder(config)
    
    try:
        # Initialize detectors with error handling
        face_detector = FaceDetector(config)
        eye_tracker = EyeTracker(config)
        mouth_monitor = MouthMonitor(config)
        multi_face_detector = MultiFaceDetector(config)
        object_detector = ObjectDetector(config)
        
        # Set alert logger for all detectors
        detectors = [face_detector, eye_tracker, mouth_monitor, 
                    multi_face_detector, object_detector]
        
        for detector in detectors:
            if hasattr(detector, 'set_alert_logger'):
                detector.set_alert_logger(alert_logger)

        # Start video capture
        cap = cv2.VideoCapture(config['video']['source'])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['video']['resolution'][0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['video']['resolution'][1])
        
        video_recorder.start_recording()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            try:
                # Perform all detections
                face_present = face_detector.detect_face(frame)
                gaze_direction, eye_ratio = eye_tracker.track_eyes(frame)
                mouth_moving = mouth_monitor.monitor_mouth(frame)
                multiple_faces = multi_face_detector.detect_multiple_faces(frame)
                objects_detected = object_detector.detect_objects(frame, visualize=True)
                
                # Display detection results
                display_detection_results(frame, face_present, gaze_direction, 
                                        eye_ratio, mouth_moving, multiple_faces,
                                        objects_detected)
                
                # Record frame
                video_recorder.record_frame(frame)
                
                # Show frame
                cv2.imshow('Exam Monitoring', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            except Exception as e:
                alert_logger.log_alert(
                    "DETECTION_ERROR",
                    f"Error in detection pipeline: {str(e)}"
                )
                continue
                
    except Exception as e:
        alert_logger.log_alert(
            "SYSTEM_ERROR",
            f"System initialization failed: {str(e)}"
        )
    finally:
        cap.release()
        video_recorder.stop_recording()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()