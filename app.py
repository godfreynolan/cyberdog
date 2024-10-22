import subprocess
import soundfile as sf
import config as config
import numpy as np
import threading
import signal

sample_rate = 44100
channels = 1
RTSP_URL = "rtsp://127.0.0.1:8554/video_stream"  # Change to stream IP
audio_filename = 'recording.wav'
audio_file = None
process = None
stop_flag = threading.Event()

def capture_audio_stream():
    global process
    try:
        process = subprocess.Popen(
            ['ffmpeg', '-rtsp_transport', 'tcp', '-i', RTSP_URL, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '1',
             '-f', 'wav', 'pipe:1', '-loglevel', 'error', '-buffer_size', '1000000', '-tune', 'zerolatency'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return process
    except Exception as e:
        print(f"Error initializing FFmpeg: {e}")
        return None

def start_recording():
    global audio_file, process
    try:
        process = capture_audio_stream()
        if process is None or process.stdout is None:
            return

        print("Recording started...")

        audio_file = sf.SoundFile(audio_filename, mode='w', samplerate=sample_rate, channels=channels)

        while not stop_flag.is_set():
            audio_data = process.stdout.read(16384)
            if not audio_data:
                break

            try:
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                if audio_file is not None:
                    audio_file.write(audio_array)
            except Exception as e:
                break

    except Exception as e:
        print(f"An error occurred during recording: {e}")
    finally:
        if audio_file is not None:
            audio_file.close()
            audio_file = None
            print("Audio file closed.")

def handle_exit_signal(signum, frame):
    global stop_flag
    stop_flag.set()

    if process is not None:
        process.terminate()
        process.kill()

def main():
    signal.signal(signal.SIGTERM, handle_exit_signal)
    signal.signal(signal.SIGINT, handle_exit_signal)

    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()

    try:
        recording_thread.join()
    except KeyboardInterrupt:
        handle_exit_signal(None, None)

if __name__ == "__main__":
    main()