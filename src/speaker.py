import pyttsx3

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Set properties if needed (e.g., rate, volume)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

    def speak(self, text):
        """Speaks the given text."""
        print(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    speaker = Speaker()
    speaker.speak("Hello, I am your visual assistant.")
