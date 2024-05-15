# Audio Processing Toolkit

## Deskripsi
Toolkit pemrosesan audio ini memungkinkan pengguna untuk melakukan beberapa operasi pada file audio, termasuk konversi format, transkripsi, dan penyuntingan audio seperti mengganti kata-kata tertentu dengan suara beep. Toolkit ini menggunakan PyDub untuk manipulasi audio dan Google Cloud Speech-to-Text API untuk transkripsi.

## Fitur
- Konversi format audio dari M4A ke WAV.
- Transkripsi audio dan ekstraksi timestamp untuk kata-kata.
- Penggantian kata-kata sensitif dengan suara beep dalam file audio.
- Konfigurasi fleksibel untuk kebutuhan penggantian kata.

## Persyaratan Instalasi
Sebelum menjalankan skrip ini, pastikan Anda telah menginstal Python dan library yang diperlukan. Berikut adalah langkah-langkah untuk instalasi:

### 1. Instal Python
   Pastikan Python versi 3.9 atau lebih baru sudah terinstal di sistem Anda. Python dapat diunduh dari [python.org](https://python.org).

### 2. Instalasi Library Python
   Skrip ini memerlukan beberapa library eksternal, yang dapat diinstal menggunakan pip. Jalankan perintah berikut di terminal Anda:
   ```bash
   pip install -r requirements.txt
   ```
### 3. Instalasi Dependensi PyDub
PyDub membutuhkan FFmpeg untuk memproses beberapa format file audio. Cara instalasi FFmpeg berbeda-beda tergantung pada sistem operasi:

#### Windows:
  - Unduh build FFmpeg dari [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/) atau [BtbN GitHub](https://github.com/BtbN/FFmpeg-Builds/releases).
  - Ekstrak arsip dan tambahkan direktori `bin` ke variabel lingkungan `PATH`.

#### macOS:
  - Install FFmpeg menggunakan Homebrew dengan perintah:
    ```bash
    brew install ffmpeg
    ```

#### Linux:
  - Instal FFmpeg menggunakan package manager yang sesuai dengan distribusi Anda, contoh untuk Ubuntu:
    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```

### 4. Konfigurasi Google Cloud
   - Buat proyek di Google Cloud Platform.
   - Aktifkan API Speech-to-Text.
   - Buat 'bucket' di Google Cloud Storage (jika diperlukan).
   - Buat dan unduh kredensial JSON untuk autentikasi. Simpan file ini sebagai `GoogleCredentials.json` di direktori proyek.

## Cara Menjalankan
Setelah semua konfigurasi selesai, Anda dapat menjalankan skrip menggunakan Python:

```bash
python app_new.py
```

## Konfigurasi
- **BUCKET_NAME**: Sesuaikan dengan nama bucket Anda di Google Cloud Storage.
- **SERVICE_ACCOUNT_FILE**: Pastikan file `GoogleCredentials.json` tersimpan dengan benar di direktori yang sama dengan skrip.

## Lisensi
Proyek ini dilisensikan di bawah [MIT License](https://opensource.org/licenses/MIT).

## Kontributor
- Afif A. Iskandar

## Kontak
Untuk pertanyaan lebih lanjut, silakan hubungi [surel.afifai@gmail.com].

