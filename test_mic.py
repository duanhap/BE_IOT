import requests
import numpy as np
from pydub import AudioSegment


# =========================
# CẤU HÌNH
# =========================
MP3_FILE = "test77.mp3"  # file MP3 của bạn
SERVER_URL = "http://127.0.0.1:8000/voice"
CHUNK_SIZE = 3200       # size mỗi chunk (bytes) giả lập ESP32 gửi
# =========================

# 1️⃣ Convert MP3 -> PCM 16-bit mono 16kHz
audio = AudioSegment.from_mp3(MP3_FILE)
audio = audio.set_channels(1).set_frame_rate(16000)
samples = np.array(audio.get_array_of_samples(), dtype=np.int16)
raw_data = samples.tobytes()
print(f"[INFO] Đã convert {MP3_FILE} -> raw PCM ({len(raw_data)} bytes)")

# 2️⃣ Gửi từng chunk lên /chunk - SỬA LẠI Ở ĐÂY
print("[INFO] Gửi chunk lên server...")
for i in range(0, len(raw_data), CHUNK_SIZE):
    chunk = raw_data[i:i+CHUNK_SIZE]
    
    # SỬA QUAN TRỌNG: Gửi raw binary data, không dùng files parameter
    headers = {'Content-Type': 'application/octet-stream'}
    resp = requests.post(f"{SERVER_URL}/chunk", data=chunk, headers=headers)
    
    if resp.status_code != 200:
        print(f"[ERROR] Chunk {i//CHUNK_SIZE} lỗi: {resp.status_code} - {resp.text}")
        break
    else:
        print(f"[OK] Chunk {i//CHUNK_SIZE} gửi xong - {resp.json()}")

# 3️⃣ Gọi /finalize để xử lý
print("[INFO] Gọi /finalize để Whisper + lưu DB + publish MQTT...")

# Gọi finalize
resp = requests.post(f"{SERVER_URL}/finalize")
if resp.status_code == 200:
    print("[RESULT] ", resp.json())
else:
    print("[ERROR FINALIZE] ", resp.status_code, resp.text)
# Thêm vào cuối file test_mic.py để debug
