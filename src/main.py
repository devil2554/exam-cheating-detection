import cv2
import yaml
from datetime import datetime
from detection.face_detection import FaceDetector
from detection.eye_tracking import EyeTracker
from detection.mouth_detection import MouthMonitor
from detection.object_detection import ObjectDetector
from detection.multi_face import MultiFaceDetector
from detection.audio_detection import AudioMonitor
from utils.video_utils import VideoRecorder
from utils.screen_capture import ScreenRecorder
from utils.logging import AlertLogger
from utils.alert_system import AlertSystem
from utils.violation_logger import ViolationLogger
from utils.screenshot_utils import ViolationCapturer
from reporting.report_generator import ReportGenerator


def load_config():
    with open('config/config.yaml') as f:
        return yaml.safe_load(f)

def display_detection_results(frame, results):
    y_offset = 30
    line_height = 30
    
    # Status indicators
    status_items = [
        f"Face: {'Present' if results['face_present'] else 'Absent'}",
        f"Gaze: {results['gaze_direction']}",
        f"Eyes: {'Open' if results['eye_ratio'] > 0.25 else 'Closed'}",
        f"Mouth: {'Moving' if results['mouth_moving'] else 'Still'}"
    ]
    
    # Alert indicators
    alert_items = []
    if results['multiple_faces']:
        alert_items.append("Multiple Faces Detected!")
    if results['objects_detected']:
        alert_items.append("Suspicious Object Detected!")

    # Display status
    for item in status_items:
        cv2.putText(frame, item, (10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        y_offset += line_height
    
    # Display alerts
    for item in alert_items:
        cv2.putText(frame, item, (10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        y_offset += line_height
    
    # Timestamp
    cv2.putText(frame, results['timestamp'], 
               (frame.shape[1] - 250, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

def main():
    config = load_config()
    alert_logger = AlertLogger(config)
    alert_system = AlertSystem(config)
    violation_capturer = ViolationCapturer(config)
    violation_logger = ViolationLogger(config)
    report_generator = ReportGenerator(config)

    student_info = {
        'id': 'STUDENT_001',
        'name': 'John Doe',
        'exam': 'Final Examination',
        'course': 'Computer Science 101'
    }

    
    # Initialize recorders
    video_recorder = VideoRecorder(config)
    screen_recorder = ScreenRecorder(config)
    
    # Initialize audio monitor
    audio_monitor = AudioMonitor(config)
    audio_monitor.alert_system = alert_system
    audio_monitor.alert_logger = alert_logger

    if config['detection']['audio_monitoring']:
        audio_monitor.start()

    try:
        if config['screen']['recording']:
            screen_recorder.start_recording()
        # Initialize detectors
        detectors = [
            FaceDetector(config),
            EyeTracker(config),
            MouthMonitor(config),
            MultiFaceDetector(config),
            ObjectDetector(config),
        ]
        
        for detector in detectors:
            if hasattr(detector, 'set_alert_logger'):
                detector.set_alert_logger(alert_logger)

        # Start webcam recording
        video_recorder.start_recording()
        cap = cv2.VideoCapture(config['video']['source'])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['video']['resolution'][0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['video']['resolution'][1])
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            results = {
                'face_present': False,
                'gaze_direction': 'Center',
                'eye_ratio': 0.3,
                'mouth_moving': False,
                'multiple_faces': False,
                'objects_detected': False,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Perform detections
            results['face_present'] = detectors[0].detect_face(frame)
            results['gaze_direction'], results['eye_ratio'] = detectors[1].track_eyes(frame)
            results['mouth_moving'] = detectors[2].monitor_mouth(frame)
            results['multiple_faces'] = detectors[3].detect_multiple_faces(frame)
            results['objects_detected'] = detectors[4].detect_objects(frame)

            if not results['face_present']:
                violation_type = "FACE_DISAPPEARED"
                alert_system.speak_alert(violation_type)
                
                # Capture and log violation
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                violation_image = violation_capturer.capture_violation(frame, violation_type, timestamp)
                violation_logger.log_violation(
                    violation_type,
                    timestamp,
                    {'duration': '5+ seconds', 'frame': results}
                )
                # alert_system.speak_alert("FACE_DISAPPEARED")
            elif results['multiple_faces']:
                violation_type = "MULTIPLE_FACES"
                alert_system.speak_alert(violation_type)
                
                # Capture and log violation
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                violation_image = violation_capturer.capture_violation(frame, violation_type, timestamp)
                violation_logger.log_violation(
                    violation_type,
                    timestamp,
                    {'duration': '5+ seconds', 'frame': results}
                )
                # alert_system.speak_alert("MULTIPLE_FACES")
            elif results['objects_detected']:
                violation_type = "OBJECT_DETECTED"
                alert_system.speak_alert(violation_type)
                
                # Capture and log violation
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                violation_image = violation_capturer.capture_violation(frame, violation_type, timestamp)
                violation_logger.log_violation(
                    violation_type,
                    timestamp,
                    {'duration': '5+ seconds', 'frame': results}
                )
                # alert_system.speak_alert("OBJECT_DETECTED")
            # elif results['gaze_direction'] != "Center":
            #     violation_type = "GAZE_AWAY"
            #     alert_system.speak_alert(violation_type)
                
            #     # Capture and log violation
            #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            #     violation_image = violation_capturer.capture_violation(frame, violation_type, timestamp)
            #     violation_logger.log_violation(
            #         violation_type,
            #         timestamp,
            #         {'duration': '5+ seconds', 'frame': results}
            #     )
                # alert_system.speak_alert("GAZE_AWAY")
            elif results['mouth_moving']:
                violation_type = "MOUTH_MOVING"
                alert_system.speak_alert(violation_type)
                
                # Capture and log violation
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                violation_image = violation_capturer.capture_violation(frame, violation_type, timestamp)
                violation_logger.log_violation(
                    violation_type,
                    timestamp,
                    {'duration': '5+ seconds', 'frame': results}
                )
                # alert_system.speak_alert("MOUTH_MOVING")

            
            # Display and record
            display_detection_results(frame, results)
            video_recorder.record_frame(frame)
            
            # Show preview
            cv2.imshow('Exam Proctoring', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        violations = violation_logger.get_violations()
        report_path = report_generator.generate_report(student_info, violations)
        print(f"Report generated: {report_path}")
        if config['screen']['recording']:
            screen_data = screen_recorder.stop_recording()
            print(f"Screen recording saved: {screen_data['filename']}")
        
        video_data = video_recorder.stop_recording()
        print(f"Webcam recording saved: {video_data['filename']}")
        
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()