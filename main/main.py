import re
import speech_recognition as sr
import AppOpener
import wikipediaapi
import webbrowser
import pyttsx3
import urllib.parse

# Initialize the recognizer and the speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()


## Features

# Function to open an application
def open_app(text):
    app_name = text.replace("open", "").strip()
    try:
        AppOpener.open(app_name, match_closest=True, throw_error=True)
        speak(f"opening {app_name}")
    except AppOpener.features.AppNotFound:
        speak("The application is not on your device.", text=True)

# Function to close an application
def close_app(text):
    app_name = text.replace("close", "").strip()
    try:
        AppOpener.close(app_name, throw_error=True)
        speak(f"CLOSING {app_name}", text=True)
    except AppOpener.features.AppNotFound:
        speak("The application is not running.", text=True)

# Function to search on Web browser
def web_search(text):
    search_term = text.replace("search", "").strip()
    script = f"Searching {search_term} on web browser"
    speak(script, text=True)
    query = urllib.parse.quote(search_term)
    web_search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(web_search_url)

# Function to search on Wikipedia
def wiki_search(text):
    search_term = text.strip("search").rstrip("on wikipedia")
    
    wiki_wiki = wikipediaapi.Wikipedia("Voice Assistant")
    page = wiki_wiki.page(search_term)
    
    if page.exists():
        script = f"Opening Wikipedia page for: {search_term}"
        speak(script, text=True)
        print("Page URL:", page.fullurl)
        webbrowser.open(page.fullurl)
    else:
        script = f"{search_term} not found on WikiPedia"
        speak(script, text=True)
    

## System

# Function to capture audio from the microphone
def capture_audio(output=True, a_speech_time=3):
    with sr.Microphone() as source:
        if output:
            print("\nListening...\n")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=a_speech_time)
        return audio

# Function to transcribe speech using Google Speech Recognition
def transcribe_speech(audio, output=True, error=True):
    try:
        text = recognizer.recognize_google(audio)
        if output:
            print(f"Your Speech: {text}")
        return text
    except sr.UnknownValueError:
        if error:
            print("Cannot hear clearly.")
    except sr.RequestError as e:
        script = "Please check your internet connection."
        speak(script, text=True)
    return ""


# Function to speak to the user
def speak(script, text=False):
    engine.say(script)
    if text:
        print(script)
    engine.runAndWait()

# Function to check for exit commands
def is_exit(text):
    if 'exit' in text or 'quit' in text:
        script = "Exiting program..."
        speak(script, text=True)
        exit()

# Function to check if the text is a math quiz
def is_math_qz(text):
    try:
        result = eval(text)
        speak(f"{text} = {result}", text=True)
    except Exception:
        print("\nSyntaxError")


# Function to guide the flow of the program
def guide_flow(text):
    pattern = r"(?:open|close|search)\s.+"
    if re.search(pattern, text):
        if "open" in text:
            open_app(text)
        elif "close" in text:
            close_app(text)
        elif re.search(r".+on\swiki(?:pedia)?", text):
            wiki_search(text)
        elif "search" in text:
            speak("SEARCHING", text=True)
            web_search(text)
    elif re.match(r"^[\d\s\+\-\*\/\(\)\.]+$", text):
        is_math_qz(text)


# Function to respond to the user
def respond(start=False):
    while start:
        audio_input = capture_audio(output=True)
        if audio_input:
            text = transcribe_speech(audio_input).lower()
            is_exit(text)
            
            if "pause" in text or "stop" in text:
                speak("Paused for a while.", text=True)
                # Switch to background process
                main()
                # Break innter loop to prevent loopings
                break
            guide_flow(text)


# Main function to activate the voice assistant
def main(text=True):
    print("Say 'HELLO' to activate the voice assistant! Otherwise 'PAUSE' or 'STOP'.")
    while True:
        audio = capture_audio(output=False, a_speech_time=3)
        text = transcribe_speech(audio, error=False).lower()
        if "hello" in text:
            speak("Hello, I am your assistant! How can I help you?", text=True)
            respond(start=True)
        is_exit(text)

if __name__ == "__main__":
    main()