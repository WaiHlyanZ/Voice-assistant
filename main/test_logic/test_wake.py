import speech_recognition as sr

# Function to listen for wake word
def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = recognizer.listen(source)

    try:
        # Recognize wake word
        wake_word = recognizer.recognize_google(audio)
        print(wake_word)
        if "open" in wake_word:  # Adjust the wake word as needed
            return False
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    return True

# Function to record user input
def record_user_input(duration):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=duration)

    try:
        # Recognize user input
        user_input = recognizer.recognize_google(audio)
        print(user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    return None

# Main function
def main():
    # Listen for wake word
    while not listen_for_wake_word():
        pass

    # Wake word detected, record user input
    user_input = record_user_input(duration=5)  # Record for 5 seconds

    if user_input:
        print("User input:", user_input)
        # Further process user input (e.g., open/close an app)

if __name__ == "__main__":
    main()
