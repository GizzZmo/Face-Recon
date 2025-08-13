import speech_recognition as sr

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Si passordsetningen:")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Ukjent stemme"

if recognize_voice() == "Godkjent frase":
    print("Adgang tillatt!")
