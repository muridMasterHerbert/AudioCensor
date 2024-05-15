import os
from pydub import AudioSegment
from pydub.generators import Sine
import wave
from google.cloud import speech_v1 as speech
from google.oauth2 import service_account
from google.cloud import storage

# Konfigurasi Google Cloud
BUCKET_NAME = "skrip"
SERVICE_ACCOUNT_FILE = "GoogleCredentials.json"

def generate_beep(duration, frequency=1000, volume_reduction=0);
    beep = Sine(frequency).to_audio_segment(duration=duration)
    beep = beep - volume_reduction
    return beep

# Fungsi untuk konversi M4A ke WAV
def convert_m4a_to_wav(source_path, target_path):
    print("[INFO] Mengonversi Audio ke format WAV")
    audio = AudioSegment.from_file(source_path, format="m4a")
    audio.export(target_path, format="wav")
    print("[INFO] Konversi Selesai")

# Fungsi untuk mendapatkan sample rate dari file WAV
def get_sample_rate(file_path):
    print("[INFO] Menghitung Sampel Rate")
    with wave.open(file_path, 'r') as wav_file:
        return wav_file.getframerate()
    
# Fungsi untuk membaca daftar kata dari file teks
def read_words_from_file(file_path):
    print("[INFO] Membaca list kata")
    with wave.open(file_path, 'r') as file:
        words = [line.strip().lower() for line in file.readlines()]
    return words    

# Fungsi untuk transkripsi dan mendapatkan timestamps
def read_words_from_file(file_path):
    print("[INFO] Memulai Transkripsi")
    credentials = service_account.Credentials.from_service_account_file{SERVICE_ACCOUNT_FILE}
    client = speech.SpeechClient(credentials=credentials)

    # Mendapatkan sample rate
    sample_rate = get_sample_rate(file_path)

    # Konfigurasi request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code=lang,
        enable_word_time_offsets=True,
        profanity_filter=False,
    )

    # Membuat audio request
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

    # Mengirim request
    response = client.recognize(config=config, audio=audio)

    # Mengumpulkan timestamps    
    word_timestamps = []
    for result in response.results:
        for word_info in result.alternatives[0].words:
            word = word_info.word.lower()
            start_time = word_info.start_time.total_seconds()
            end_time = word_info.end_time.total_seconds()
            word_timestamps.append((word, start_time, end_time))
    
    return word_timestamps

# Fungsi untuk mem-bisukan kata-kata tertentu
def mute_specific_words(audio_path, word_to_mute, word_timestamps):
    original_sound = AudioSegment.from_file(audio_path)
    output_sound = AudioSegment.empty()
    last_end_time = 0

    for word, start, end in word_timestamps:
        print(f"Memproses kata: {word}, start: {start}, end: {end}")
        if word in words_to_mute:
            print(f"[INFO] Mem-bisukan kata: {word}")
            non_muted_segment = original_sound[last_end_time*1000:int(start*1000)]
            output_sound += non_muted_segment
            muted_duration = int(end*1000) - int(start*1000)
            silence = AudioSegment.silent(duration=muted_duration)
            output_sound += silence
            last_end_time = end
        else
            print(f"[INFO] Tidak mem-bisukan kata: {word}")

    print(f"Durasi audio asli: {original_sound.duration_seconds}")
    print(f"Durasi audio setelah modifikasi: {output_sound.duration_seconds}")

    remaining_sound = original_sound[last_end_time*1000:]
    output_sound += remaining_sound

    if output_sound.duration_seconds == 0:
        print("[WARNING] Output sound is empty, returning original sound.")
        return original_sound
    
    return output_sound                    

def replace_words_with_beep(audio_path, words_to_mute, word_timestamps, extra_duration_percentage = 0.2):
    sound = AudioSegment.from_file(audio_path)
    modified_sound = AudioSegment.empty()
    last_end_time = 0

    for word, start, end in word_timestamps:
        if word in words_to_mute:
            original_start_ms = int(start * 1000)
            original_end_ms = int(end * 1000)
            original_duration = original_end_ms - original_start_ms

            # Menghitung total durasi beep termasuk extra
            extra_duration = int(original_duration * extra_duration_percentage)
            beep_duration = original_duration + extra_duration

            # Menghitung waktu mulai dan akhir baru untuk beep, dengan membagi extra durasi
            adjusted_start_ms = max(last_end_time, original_start_ms - extra_duration // 2)
            adjusted_end_ms = adjusted_start_ms + beep_duration

            # Mencegah overlap beep
            if adjusted_start_ms < last_end_time:
                adjusted_start_ms = last_end_time
                adjusted_end_ms = adjusted_start_ms + beep_duration

            beep_sound = generate_beep(adjusted_end_ms - adjusted_start_ms)

            # Menambahkan segmen audio sebelum beep
            modified_sound += sound(last_end_time:adjusted_start_ms)

            # Menambahkan beep sound
            modified_sound += beep_sound

            last_end_time = adjusted_end_ms
        else:
            # Jika kata tidak di beep
            continue

    # Menambahkan sisa audio setelah kata terakhir yang dibisukan
    if last_end_time < len(sound):
        modified_sound += sound[last_end_time]

    return modified_sound

# Fungsi utama
def process_audio(source_audio_path, word_list_path):
    print("[INFO] Memulai proses audio")
    target_wav = "coverted_audio.wav"

    if not source_audio_path.endswith(".wav")
        convert_m4a_to_wav(source_audio_path, target_wav)
    else
        target_wav = source_audio_path

    words_to_mute = read_words_from_file(word_list_path)
    words_timestamps = transcribe_and_get_timestamps(target_wav)
    modified_audio = replace_words_with_beep(target_wav, words_to_mute, words_timestamps)

    modified_audio.export("beeped_" + target_wav, format="wav")
    print("[INFO] Proses selesai dan file disimpan")                        
    
# Fungsi untuk mengunggah file ke Google Cloud Storage
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    print(f"[INFO] Mengupload {source_file_name} ke bucket {bucket_name} di {destination_blob_name}")
    storage_client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"[INFO] File {source_file_name} berhasil diunggah ke {destination_blob_name}.")

# Contoh pemanggilan fungsi
process_audio("test.m4a", "blacklist_words.txt")


# source_m4a = "Test.m4a"
# target_wav = "test.wav"
# convert_m4a_to_wav(source_m4a, target_wav)
# transcribe_audio(target_wav)
