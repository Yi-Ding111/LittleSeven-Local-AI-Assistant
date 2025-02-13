import pyttsx3


# EN
def text_to_speech_offline(text):
    engine = pyttsx3.init()

    engine.setProperty("volume", 1.0)
    engine.setProperty("rate", 180)

    engine.setProperty("voice", "com.apple.speech.synthesis.voice.samantha")

    engine.say(text)
    engine.runAndWait()


