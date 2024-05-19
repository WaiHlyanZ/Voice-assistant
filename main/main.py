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
def transcribe_speech(audio, output=True):
    try:
        text = recognizer.recognize_google(audio)
        if output:
            print(f"Your Speech: {text}")
        return text
    except sr.UnknownValueError:
        print("Cannot hear clearly.")
    except sr.RequestError as e:
        script = "Please check your internet connection."
        speak(script, text=True)
        print(f"Error fetching results: {e}")
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
    pattern = r"(^\d+\.?(?:\d+)?\s[\+\-\*\/]{1}\s\d+\.?(?:\d+)?$)"
    if match := re.search(pattern, text):
        result = eval(match.group(1))
        speak(f"{match.group(1)} = {result}", text=True)


# Function to guide the flow of the program
def guide_flow(text):
    pattern = r"(?:open|close|search)\s.+"
    if re.search(pattern, text):
        if "open" in text:
            open_app(text)
        elif "close" in text:
            close_app(text)
        elif "search" in text:
            speak("SEARCHING", text=True)
            search(text)

# Function to respond to the user
def respond(start=False):
    while start:
        audio_input = capture_audio(output=True)
        if audio_input:
            text = transcribe_speech(audio_input).lower()
            is_exit(text)
            is_math_qz(text)
            if "pause" in text or "stop" in text:
                speak("Paused for a while.", text=True)
                # Switch to background process
                main()
                # Break innter loop to prevent loopings
                break
            guide_flow(text)

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

# Function to search on Wikipedia or Web browser
def search(text):
    search_term = text.replace("search", "").strip()
    wiki_wiki = wikipediaapi.Wikipedia("Voice Assistant")
    page = wiki_wiki.page(search_term)
    
    if page.exists():
        script = f"Opening Wikipedia page for: {search_term}"
        speak(script, text=True)
        print("Page URL:", page.fullurl)
        webbrowser.open(page.fullurl)
    else:
        script = f"Wikipedia page not found for: {search_term}. Performing a web search instead."
        speak(script, text=True)
        query = urllib.parse.quote(search_term)
        web_search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(web_search_url)

# Main function to activate the voice assistant
def main(text=True):
    print("Say 'HELLO' to activate the voice assistant! Otherwise 'PAUSE' or 'STOP'.")
    while True:
        audio = capture_audio(output=False, a_speech_time=5)
        text = transcribe_speech(audio).lower()
        if "hello" in text:
            speak("Hello, I am your assistant! How can I help you?", text=True)
            respond(start=True)
        is_exit(text)

if __name__ == "__main__":
    main()