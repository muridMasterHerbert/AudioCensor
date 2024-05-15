import os
from pydub import AudioSegment
import wave
from google.cloud import speech_v1 as speech
from google.oauth2 import service_account
from google.cloud import storage

# Konfigurasi Google Cloud
BUCKET_NAME = "skrip"
SERVICE_ACCOUNT_FILE = "GoogleCredentials.json"

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

# Fungsi untuk mengunggah file ke Google Cloud Storage
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    print(f"[INFO] Mengupload {source_file_name} ke bucket {bucket_name} di {destination_blob_name}")
    storage_client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"[INFO] File {source_file_name} berhasil diunggah ke {destination_blob_name}.")

# Fungsi utama untuk transkripsi audio
def transcribe_audio(file_path, lang="id-ID"):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = speech.SpeechClient(credentials=credentials)
    
    # Cek ukuran file untuk menentukan metode transkripsi
    file_size = os.path.getsize(file_path)
    sample_rate = get_sample_rate(file_path)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code=lang,
        enable_word_time_offsets=True,
        profanity_filter=False,
    )
    
    if file_size < 10 * 1024 * 1024:  # Ukuran file kurang dari 10 MB
        with open(file_path, "rb") as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
        response = client.recognize(config=config, audio=audio)
    else:
        # Ukuran file lebih dari 10 MB, gunakan Google Cloud Storage
        destination_blob_name = os.path.basename(file_path)
        upload_blob(BUCKET_NAME, file_path, destination_blob_name)
        gcs_uri = f"gs://{BUCKET_NAME}/{destination_blob_name}"
        audio = speech.RecognitionAudio(uri=gcs_uri)
        operation = client.long_running_recognize(config=config, audio=audio)
        print("Menunggu operasi selesai...")
        response = operation.result(timeout=900)  # Timeout 15 menit

    # Menampilkan hasil transkripsi
    for result in response.results:
        print("Transkripsi:", result.alternatives[0].transcript)

    # for result in response.results:
        print("Transkripsi:", result.alternatives[0].transcript)
        for word_info in result.alternatives[0].words:
            print(f'Kata: {word_info.word}, mulai pada: {word_info.start_time.total_seconds()} detik, berakhir pada: {word_info.end_time.total_seconds()} detik')

# Contoh penggunaan
source_m4a = "Test.m4a"
target_wav = "test.wav"
convert_m4a_to_wav(source_m4a, target_wav)
transcribe_audio(target_wav)
