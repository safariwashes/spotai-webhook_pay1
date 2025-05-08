from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'spotai_data.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS plate_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT,
            timestamp TEXT,
            camera_id TEXT,
            raw_payload TEXT,
            created_on TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/spotai-webhook', methods=['POST'])
def spotai_webhook():
    data = request.get_json()
    plate = data.get('plate')
    camera_id = data.get('camera_id')
    timestamp = data.get('timestamp')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO plate_logs (plate, timestamp, camera_id, raw_payload, created_on)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        plate,
        timestamp,
        camera_id,
        str(data),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
