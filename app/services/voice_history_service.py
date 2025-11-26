import os
import wave
import numpy as np
from datetime import datetime

import whisper
from app.repositories.device_repository import DeviceRepository
from app.repositories.voice_history_repository import VoiceHistoryRepository
from app.services.device_history_service import DeviceHistoryService
from sqlalchemy.orm import Session
from app.mqtt.mqtt_service import publish

import time
class VoiceHistoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = VoiceHistoryRepository(db)
        self.device_repo = DeviceRepository(db)

    def detect_language(self, raw_data: bytes) -> str:
        """
        Detect language from short audio using Whisper
        """
        from app.routers.voice_routes import model
        
        try:
            # Convert raw bytes to numpy array
            audio_array = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # For short audio, we need to pad it to at least 1 second
            target_length = 16000  # 1 second at 16kHz
            if len(audio_array) < target_length:
                # Pad with silence
                silence_length = target_length - len(audio_array)
                audio_array = np.pad(audio_array, (0, silence_length))
            else:
                audio_array = audio_array[:target_length]
            
            # Pad to 30 seconds for Whisper (required for language detection)
            padded_audio = np.pad(audio_array, (0, 30 * 16000 - len(audio_array)))
            
            # Detect language
            mel = whisper.log_mel_spectrogram(padded_audio).to(model.device)
            _, probs = model.detect_language(mel)
            detected_lang = max(probs, key=probs.get)
            confidence = probs[detected_lang]
            
            print(f"🎯 [LANGUAGE DETECTION] Detected: {detected_lang} (confidence: {confidence:.2%})")
            
            # Map to supported languages
            language_map = {
                'en': 'en',  # English
                'vi': 'vi',  # Vietnamese
                'fr': 'fr',  # French
                'es': 'es',  # Spanish
                'de': 'de',  # German
                'zh': 'zh',  # Chinese
                'ja': 'ja',  # Japanese
                'ko': 'ko'   # Korean
            }
            
            # Only return if confidence is high enough
            if confidence > 0.1:  # 10% threshold for short audio
                return language_map.get(detected_lang, 'en')
            else:
                return 'en'  # Default to English
            
        except Exception as e:
            print(f"❌ [LANGUAGE DETECTION ERROR] {e}")
            return 'en'  # Default to English on error

    def process_voice(self, raw_data: bytes, language: str = None):
        from app.routers.voice_routes import model

        """
        1. Detect language if not provided
        2. Convert raw PCM -> proper WAV
        3. Transcribe Whisper
        """
        
        # ---- Detect language if not provided ----
        if language is None:
            language = self.detect_language(raw_data)
            print(f"🔊 Using language: {language}")

        tmp_wav = f"uploads/{datetime.utcnow().timestamp()}_high_quality.wav"
        os.makedirs("uploads", exist_ok=True)
        
        # Convert PCM to proper WAV với chất lượng tốt nhất
        self.create_high_quality_wav(raw_data, tmp_wav)
        
        # ---- Transcribe với parameters tối ưu ----
        print(f"🎤 Transcribing high quality audio...")
        
        # Sử dụng parameters giống như Flask app
        result = model.transcribe(
            tmp_wav,
            language=language,
            task="transcribe",
            fp16=False,  # Dùng FP32 để ổn định
            no_speech_threshold=0.6,
            logprob_threshold=-1.0,
            compression_ratio_threshold=2.4
        )
        
        text = result["text"].strip()
        print(f"📝 Transcribed text: '{text}'")
        
        # Thêm task và các tham số để cải thiện chất lượng
        result = model.transcribe(
            tmp_wav, 
            language=language,
            task="transcribe",
            fp16=False,  # Force FP32 for better compatibility
            no_speech_threshold=0.6  # Giảm threshold cho audio ngắn
        )
        
        text = result["text"].strip()
        print(f"📝 Transcribed text: '{text}'")

        # ---- xác định action + device ----
        action = None
        device_obj = None
        text_lower = text.lower()

        devices = self.device_repo.get_all()
        for d in devices:
            if language == "vi":
                if d.name_vn and d.name_vn.lower() in text_lower:
                    device_obj = d
                    break
            else:
                if d.name and d.name.lower() in text_lower:
                    device_obj = d
                    break

        # action map
        action_map = {
            "turn on": "on", "turn off": "off", "on": "on", "off": "off",
            "bật": "on", "tắt": "off", "mở": "on", "đóng": "off"
        }
        for k, v in action_map.items():
            if k in text_lower:
                action = v
                break

        # ---- publish MQTT nếu valid ----
        if device_obj and action:
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>> Publishing MQTT: {device_obj.name} -> {action}")
            start_time = time.time()
            publish(device_obj.name, action)
            end_time = time.time()
            print(f"MQTT published in {end_time - start_time:.3f} seconds")
            # update device status
            device_obj.status = action
            self.device_repo.update(device_obj)
        device_history_service = DeviceHistoryService(self.db)
        device_history_service.create_history(
            device_id=device_obj.id if device_obj else None,
            action_type=action,
            action_value=None,
            triggered_by="voice"
        )
        # ---- lưu VoiceHistory ----
        history_data = {
            "raw": text,
            "device_id": device_obj.id if device_obj else None,
            "action_name": action,
            "created_at": datetime.utcnow(),
            "processed_at": datetime.utcnow()
        }
        history = self.repository.create(history_data)

        # cleanup
        try:
            os.remove(tmp_raw)
            os.remove(tmp_wav)
        except:
            pass

        return {
            "history_id": history.id,
            "text": text,
            "device": device_obj.name if device_obj else None,
            "action": action,
            "language": language  # Thêm thông tin ngôn ngữ vào kết quả
        }

    def create_high_quality_wav(self, raw_data: bytes, output_path: str):
        """Tạo file WAV chất lượng cao từ PCM data"""
        import wave
        import numpy as np
        
        # Convert to numpy array
        audio_array = np.frombuffer(raw_data, dtype=np.int16)
        
        # Audio processing để cải thiện chất lượng
        processed_audio = self.enhance_audio_quality(audio_array)
        
        # Save as high quality WAV
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)      # Mono
            wav_file.setsampwidth(2)      # 16-bit
            wav_file.setframerate(16000)  # 16kHz
            wav_file.writeframes(processed_audio.tobytes())
        
        print(f"💾 Saved high quality WAV: {output_path} ({len(processed_audio)} samples)")

    def enhance_audio_quality(self, audio_array):
        """Xử lý nâng cao chất lượng audio"""
        import numpy as np
        from scipy import signal
        
        # Convert to float
        audio_float = audio_array.astype(np.float32)
        
        # 1. Normalize volume
        max_val = np.max(np.abs(audio_float))
        if max_val > 0:
            audio_float = audio_float / max_val * 0.9
        
        # 2. Remove DC offset
        audio_float = audio_float - np.mean(audio_float)
        
        # 3. High-pass filter to remove low frequency noise
        if len(audio_float) > 100:
            b, a = signal.butter(3, 80/(16000/2), btype='high')
            audio_float = signal.filtfilt(b, a, audio_float)
        
        # 4. Dynamic range compression (soft)
        compressed = np.tanh(audio_float * 2) / 2
        
        # Convert back to int16
        return (compressed * 32767).astype(np.int16)