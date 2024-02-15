import sys
sys.path.append('./yolov7')
from yolov7.detect_web import YoloDetect
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

import os



app = Flask(__name__)
socketio = SocketIO(app)

message_status = "Welcome! No image received yet."
weights = './yolov7/runs/test/yolov7.pt'  # 替換為你的權重檔路徑
yolo = YoloDetect(weights_path=weights)

@app.route("/")
def home():
    return message_status

@app.route('/upload', methods=['POST'])
def upload_file():
    global message_status
    # 確保資料夾存在
    os.makedirs('temp_single_image', exist_ok=True)
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        full_path = os.path.join('temp_single_image', file.filename)
        file.save(full_path)
        result = (yolo.detect(source=full_path))
        message_status = f"Received image: {file.filename}"
        # 使用SocketIO發送消息更新
        socketio.emit('message', {'msg': message_status})
        return jsonify({"message": result})

@app.route('/upload_batch', methods=['POST'])
def upload_batch():
    total_images = request.form.get('total_images')  # client發送的圖片總數
    images_received = 0

    # 確保資料夾存在
    os.makedirs('temp_image', exist_ok=True)

    for file_key in request.files:
        file = request.files[file_key]
        if file:
            file.save(os.path.join('temp_image', file.filename))
            images_received += 1

    # 使用SocketIO發送消息更新
    message_status = f"Batch upload completed: {images_received}/{total_images} images received."
    result = yolo.detect(source='temp_image')
    socketio.emit('message', {'msg': message_status })    
    return jsonify({"message": result})

if __name__ == '__main__':    
    socketio.run(app, debug=True)
