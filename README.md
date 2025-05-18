# AI-Powered Online Exam Cheating Detection System

<!-- ![System Demo](demo.gif) Add a demo gif later -->

A computer vision system that detects suspicious activities during online exams using webcam footage.

## Features

- **Face Presence Detection**: Identifies when student's face is not visible
- **Eye Movement Tracking**: Detects excessive eye movements (left/right/up/down)
- **Gaze Analysis**: Monitors direction of eye gaze
- **Mouth Movement Detection**: Identifies potential talking or whispering
- **Multi-Face Detection**: Alerts when multiple faces appear in frame
- **Real-time Alerts**: Flags suspicious activities with timestamps
- **Dashboard**: Visual interface showing detection metrics and alerts
- **Object Delection**: Object Detection: Detects prohibited objects (cell phone, book, etc.).
- **Screen Recoding**: Continuously captures examinee's screen activity
- **Audio Detection**: Monitors for voice/whispering in student's environment
- **Alert Speaker**: Delivers real-time verbal warnings via text-to-speech
- **Report Generation**: Creates detailed visual PDF and HTML reports with violations summary, heatmaps, and activity timeline  


## Technologies Used

- Python 3.8+
- OpenCV (for computer vision)
- MediaPipe (for face mesh and landmark detection)
- FaceNet-PyTorch (for face detection)
- MTCNN (for face detection)
- Flask (for dashboard)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/exam-cheating-detection.git
cd exam-cheating-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download pre-trained models (if needed):
```bash
python -c "from facenet_pytorch import MTCNN; MTCNN(keep_all=True)"
```

## Usage

1. Configure the system by editing `config/config.yaml`:
```yaml
video:
  source: 0                   # 0 for default webcam
  resolution: [1280, 720]
  fps: 30
  recording_path: "./recordings"

screen:
  monitor_index: 0           # 0 for primary monitor
  fps: 15                    # Lower FPS for screen recording
  recording: true            # Enable/disable screen recording


detection:
  face:
    detection_interval: 5     # frames
    min_confidence: 0.8
  eyes:
    gaze_threshold: 2          # seconds
    blink_threshold: 0.3       # EAR threshold for blink detection
    gaze_sensitivity: 15       # pixels threshold for gaze detection
    consecutive_frames: 3      # frames for gaze change detection
  mouth:
    movement_threshold: 3     # consecutive frames
  multi_face:
    alert_threshold: 5        # frames
  objects:
    min_confidence: 0.65  # Detection confidence threshold
    detection_interval: 5 # frames between detections
    max_fps: 5            # Maximum detection frames per second
  audio_monitoring:
    enabled: true
    sample_rate: 16000
    energy_threshold: 0.001
    zcr_threshold: 0.35
    whisper_enabled: false  # Enable only when needed
    whisper_model: "tiny.en"
        
logging:
  log_path: "./logs"
  alert_cooldown: 10          # seconds
  alert_system:
    voice_alerts: true  # Enable/disable voice alerts
    alert_volume: 0.8   # Volume level (0.0 to 1.0)
    cooldown: 10        # Minimum seconds between same alert
```

2.Run the main detection system:
```bash
python src/main.py
```

3. (Optional) Run the dashboard in another terminal:
```bash
python src/dashboard/app.py
```
4. Access the dashboard at `http://localhost:5000`

## System Architecture
```
exam_cheating_detection/
├── config/              # Configuration files
├── models/              # Pretrained models
├── src/                 # Source code
│   ├── detection/       # Detection modules
│   ├── reporting/       # Reporting application
│   ├── utils/           # Utility functions
│   ├── dashboard/       # Web dashboard
│   └── main.py          # Main application
├── logs/                # Session logs
└── recordings/          # Recorded video sessions
```

## Customization
You can adjust detection thresholds in `config/config.yaml`:
```yaml
eyes:
  gaze_threshold: 2      # seconds of gaze deviation to trigger alert
  blink_threshold: 0.3   # eye aspect ratio for blink detection

mouth:
  movement_threshold: 3  # consecutive frames of mouth movement
```

## Troubleshooting
Problem: Eye detection working, but not perfect

Solution:

    - Ensure good lighting on face
    - Remove glasses if they cause glare
    - Adjust camera position to be face-level

Problem: Book detection working, but not perfect

Solution:
    -

## Contributing
Contributions are welcome! Please open an issue or pull request for any improvements.

## License
MIT License - See [LICENSE](LICENSE) for details.

## ☕ Support the Project
If you find this project helpful, consider buying me a coffee!
[Buy Me a Coffee](https://buymeacoffee.com/aarambhdevhub)
