# Speach to text in python

## Description

In this project we are working on a car that is moved with voice. For this we want to translate our speech to text so we can later feed it into the car to follow directions.

# How to use

First you need to install the additional packages:

``` 
pip install pyaudio
pip install vosk
```
or

``` 
pip3 install pyaudio
pip3 install vosk
```

Get the vosk model with:

On linux:
```
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 model
```

On windows:
```
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip" -OutFile "vosk-model-small-en-us-0.15.zip"

Expand-Archive -Path "vosk-model-small-en-us-0.15.zip" -DestinationPath ".\model"

Rename-Item -Path ".\vosk-model-small-en-us-0.15" -NewName "model"
```

Then you can set the time period of the recording (it's 5 seconds as of now). then just run the `main.py` file by using `python main.py` or `python3 main.py`.

Then you can start your journey :3