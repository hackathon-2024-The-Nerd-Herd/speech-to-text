import os
import wave
import json
import pyaudio
from vosk import Model, KaldiRecognizer

# Check if Vosk model exists
if not os.path.exists("model"):
    print("Please download the Vosk model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit(1)

# Initialize Vosk model and recognizer
model = Model("model")
rec = KaldiRecognizer(model, 16000)  # Adjust the sample rate if necessary

# Function to record audio from microphone
def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5  # Adjust recording duration as needed

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

# Main function to perform speech recognition
def recognize_speech(audio_data):
    if isinstance(audio_data, bytes):
        rec.AcceptWaveform(audio_data)
        result = rec.FinalResult()
        result_json = json.loads(result)
        text = result_json['text']
        return text
    else:
        raise ValueError("Audio data should be bytes.")

# File to save recognized text
output_file = "recognized_text.txt"

# Main program loop
if __name__ == "__main__":
    try:
        run_once = True  # Flag to run only once
        
        while run_once:
            # Record audio from microphone
            audio_data = record_audio()

            # Perform speech recognition
            recognized_text = recognize_speech(audio_data)

            # Print and save recognized text to a file
            print("Recognized:", recognized_text)
            with open(output_file, "a") as f:
                f.write(recognized_text + "\n")
            
            run_once = False  # Set flag to False to exit after first run

    except KeyboardInterrupt:
        print("\nProgram interrupted. Closing...")

    except Exception as e:
        print(f"Error: {str(e)}")
