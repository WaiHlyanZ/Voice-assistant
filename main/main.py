import re
import speech_recognition as sr
from AppOpener import open, close
import wikipediaapi
import webbrowser

# Initialize the recognizer
recognizer = sr.Recognizer()


# Function to capture audio from the microphone
def capture_audio():
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            return audio
        except sr.WaitTimeoutError:
            print("Timeout occurred while listening.")
    
    

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
        print("Please check your internet connection.") # auto pause the listening if the user don't use this app for a while
        print("Error fetching results; {0}".format(e))

# Analize text
key_word = ["open", "close", "search", "tell", "story", "note", "type"]
def sanitize_text(text: str):
    pattern = r"\b(?:open|close|search)\s(?:\w+)"
    if match:= re.findall(pattern, text, re.IGNORECASE):
        tasks = []
        for pair in match:
            action, app = pair.lower().split()
            tasks.append((action, app))
        return tasks
    else:
        return []



# Perform an action 
def app_op(task: tuple):
    act, app = task
    if act == "open": open(app)
    if act == "close": close(app)

    

# Search Wiki
def is_search():
    pass

def search(text: str): # search Elon Muk
    
    wiki_wiki = wikipediaapi.Wikipedia("Voice Assistant")
    page = wiki_wiki.page(text)
    if page.exists():
        print("Page exists!")
        print("Opening Wikipedia page:", page.fullurl)
        webbrowser.open(page.fullurl)
    else:
        print("Page not found.")


def main():
    while True:
        audio_input = capture_audio()
        if audio_input:
            text = transcribe_speech(audio_input)
            if text: 
                tasks = sanitize_text(text)
                for task in tasks:
                    app_op(task)
                if "search" in text:
                    
                    search(text)

if __name__ == "__main__":
    main()
