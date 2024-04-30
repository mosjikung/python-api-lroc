import librosa
import requests
import io
import tempfile
import os

def calculate_bpm(audio_url):
    # ดึงไฟล์เสียงจาก URL
    response = requests.get(audio_url)
    
    # สร้าง temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(response.content)
        temp_filepath = temp_file.name
    
    # โหลดไฟล์เสียง
    y, sr = librosa.load(temp_filepath)

    # คำนวณ tempo ของเพลง
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # ลบ temporary file
    os.remove(temp_filepath)

    return tempo

bpm = calculate_bpm("https://nrc-file.xcoshop.com/stations/stations/180/filemedias/e5b527fa-767d-4e4c-9562-47f93aa42794-%E0%B8%97%E0%B8%99SPRITExGUYGEEGEE.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=iWxfdxHMxs5PoVoR%2F20231114%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231114T102711Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=77fa386906fddd9bfdd88bfda42e51d782702e247fae315e12624c0ce43d6b51")

print(bpm)