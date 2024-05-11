import re
import speech_recognition as sr
from AppOpener import open, close
import noisereduce as nr
import numpy as np
import wikipediaapi
import webbrowser
# Initialize the recognizer
recognizer = sr.Recognizer()
APP_NAME = [None]

# Function to capture audio from the microphone

def capture_audio(): ## !!! To recheck !!!
    # Initialize recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)

        # Record audio
        audio = recognizer.listen(source)

        # Convert audio data to numpy array
        audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)

        # Apply noise reduction
        reduced_noise = nr.reduce_noise(audio_data, audio.sample_rate)

        # Convert back to AudioData
        audio = sr.AudioData(reduced_noise.tobytes(), audio.sample_rate, audio.sample_width)

    return audio


# Function to transcribe speech using Google Speech Recognition
def transcribe_speech(audio):
    try:
        # Use Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print(f"Your Speech: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))


# Analize text
key_word = ["open", "close", "search", "tell", "story", "note", "type"]
def sanitize_txt(text: str):
    pattern = r"\b(?:open|close)\s(?:\w+)"
    if match:= re.findall(pattern, text, re.IGNORECASE):
        tasks = []
        for pair in match:
            action, app = pair.lower().split()
            tasks.append((action, app))

    return tasks

## End of analize
# Search Wiki ## Mine
def search(text: str):
    if "search" in text:
        wiki_wiki = wikipediaapi.Wikipedia("Voice Assistant", 'en')
        page_py = wiki_wiki.page(text)

        print("Page - Exists: %s" % page_py.exists())
        print(page_py.fullurl)
        url = webbrowser.open(page_py.fullurl)

# Perform an action 
def action(task: tuple):
    act, app = task
    if act == "open": open(app)
    if act == "close": close(app)

def main():
    while True:
        audio_input = capture_audio()
        text = transcribe_speech(audio_input)

def search():
    pass



main()