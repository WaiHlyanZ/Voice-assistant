import re
import speech_recognition as sr
import AppOpener
from AppOpener import open, close
import wikipediaapi
import webbrowser
import pyttsx3


# Initialize the recognizer
recognizer = sr.Recognizer()
engine = pyttsx3.init()

class Translate():
    # capture_adio()
    # transcribe_speech()
    ...

class Resopnse():
    # speak()
    # features
    ...
# Function to capture audio from the microphone
def capture_audio(output=True, a_speech_time=3):
    with sr.Microphone() as source:
        if output:
            print()
            print("Listening...") # reduce duration for listening to be less data to sanitize
            print()
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source, phrase_time_limit=a_speech_time)
        return audio


# Function to transcribe speech using Google Speech Recognition
def transcribe_speech(audio, ouput=True):
    try:
        # Use Google Speech Recognition
        text = recognizer.recognize_google(audio)
        if ouput:
            print(f"Your Speech: {text}")
        return text
    
    except sr.UnknownValueError:
        # Control timeout param to pause the program and catch this error 
        pass
    except sr.WaitTimeoutError:
        pause()
    except sr.RequestError as e:
        script = "Please check your internet connection."
        print(script) # auto pause the listening if the user don't use this app for a while
        speak(script) 
        print("Error fetching results; {0}".format(e))
    return ""


# Talk to user
def speak(script, text=False):
    engine.say(script)
    if text: print(script)
    engine.runAndWait()
    engine.stop()

# Pause the program
def pause(text):
    while True:
        if "name" in text:
            break
    


def search(text: str): # search Elon Musk
    search_term = text.replace("search", "").strip()  # Remove "search" keyword and  spaces

    wiki_wiki = wikipediaapi.Wikipedia("Voice Assistant")  # Set language to English, login as Voice assistant
    page = wiki_wiki.page(search_term)
    if page.exists():
        script = f"Opening Wikipedia page for: {search_term}"
        speak(script)
        print(script)
        print("Page URL:", page.fullurl)
        webbrowser.open(page.fullurl)
    else:
        script = f"Wikipedia page not found for: {search_term}"
        speak(script)
        print(script)

# Math
# def evaluate_expression(expression):
#     try:
#         # Remove non-alphanumeric characters and replace 'multiplied by' with '*'
#         cleaned_expression = re.sub(r'[^\w\s\+\-\*\/\.]', '', expression.lower())
#         cleaned_expression = cleaned_expression.replace('multiplied by', '*')
#         print(cleaned_expression)
#         # Evaluate the expression
#         return eval(cleaned_expression)
#     except Exception as e:
#         print("Error evaluating expression:", e)
def is_math_qz(text):
    pattern = r"(^\d+.?(?:\d+)?\s[\+\-\*\/]{1}\s\d+.?(?:\d+)?$)"
    if match := re.search(pattern, text):
        speak(f"'{match.group(1)}' is equal to '{eval(match.group(1))}'", text=True)

# Cleaning past actions
def clean_past_actions():
    pass

# Guiding the program flow
def guide_flow(text):
    if "open" in text: ...
    elif "close" in text: ...
    elif "search" in text: ...

# Open & Close
def features(text: str):
    if "open" in text:
        open_app = text.replace("open", "")
        
        try:
            open(open_app, match_closest=True, throw_error=True)  # To fix: actual opening app VS user's speech app ## To fix open alone
        except AppOpener.features.AppNotFound:
            speak("The application is not in you device.", text=True)
        else:
            speak(f"OPENING {open_app}")

    elif "close" in text:
        close_app = text.replace("close", "")
        try:
            close(close_app, throw_error=True) # Your Speech: close Google Chrome ## The Application is not running.

        except AppOpener.features.AppNotFound:
            speak("The Application is not running.", text=True) 
        else:
            speak(f"CLOSING {close_app}")
            
    elif "search" in text:
        speak("SEARCHING")
        search(text)        


# Exit the program
def is_exit(text):
    if 'exit' in text or 'quit' in text:
        script="Exiting program..."
        speak(script)
        exit(script)


def respond(start=False):
    while start:
        audio_input = capture_audio(output=True)
        if audio_input:
            text = transcribe_speech(audio_input).lower()
            # print(evaluate_expression(text))
            is_exit(text)
            if "pause" in text or "stop" in text: #fix that shit
                speak("Pused for a while.")
                main()
            features(text)
            is_math_qz(text)

def main():
    print("Say 'HELLO' to acivate the voice assistant! Otherwise 'PAUSE' or 'STOP'.")
    while True:
        audio = capture_audio(output=False, a_speech_time=None)
        text = transcribe_speech(audio).lower()
        if "hello" in text:
            speak("Hello I am your assistant! How can I help you?", text=True)
            respond(start=True)
        # if "pause" in text or "stop" in text:
        #     speak("Pused for a while.")
        #     main()
        is_exit(text)


if __name__ == "__main__":
    main()
    

