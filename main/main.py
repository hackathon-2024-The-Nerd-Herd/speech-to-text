import os
import wave
import json
import pyaudio
import requests  # Added for HTTP requests
from vosk import Model, KaldiRecognizer

if not os.path.exists("model"):
    print("Please download the Vosk model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit(1)

model = Model("model")
rec = KaldiRecognizer(model, 16000) 

def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5  

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Recording audio...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return b''.join(frames)

def recognize_speech(audio_data):
    if isinstance(audio_data, bytes):
        rec.AcceptWaveform(audio_data)
        result = rec.FinalResult()
        result_json = json.loads(result)
        text = result_json['text']
        return text
    else:
        raise ValueError("Audio data should be bytes.")

output_file = "../api/recognized_text.txt"

if __name__ == "__main__":
    try:
        run_once = True  
        
        while run_once:
            audio_data = record_audio()

            recognized_text = recognize_speech(audio_data)

            print("Recognized:", recognized_text)

            # POST request to Flask server
            url = "http://localhost:5000/upload-file"
            payload = {'text': recognized_text}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print("Text uploaded successfully.")
            else:
                print(f"Failed to upload text. Status code: {response.status_code}")

            run_once = False  

    except KeyboardInterrupt:
        print("\nProgram interrupted. Closing...")

    except Exception as e:
        print(f"Error: {str(e)}")
