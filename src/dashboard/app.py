from flask import Flask, render_template, jsonify
import os
import yaml
from datetime import datetime

app = Flask(__name__)

# Load configuration
with open('config/config.yaml') as f:
    config = yaml.safe_load(f)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/alerts')
def get_alerts():
    log_file = os.path.join(config['logging']['log_path'], "alerts.log")
    alerts = []
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            alerts = [line.strip() for line in f.readlines()[-10:]]  # Get last 10 alerts
            
    return jsonify(alerts)

@app.route('/api/stats')
def get_stats():
    # This would be more sophisticated in a real implementation
    return jsonify({
        'face_detected': True,
        'current_activity': 'Normal',
        'cheating_probability': 15,
        'last_alert': datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run(debug=True)