"""
Voice authentication module for Face-Recon system.

Uses Google Speech Recognition API to verify users via passphrase.
"""

import speech_recognition as sr


def recognize_voice() -> str:
    """
    Capture and recognize voice from microphone.

    Returns:
        Recognized text or "Unknown voice" on failure.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your passphrase:")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "Timeout"
        except sr.UnknownValueError:
            return "Unknown voice"
        except sr.RequestError as e:
            return f"API error: {e}"


def authenticate_voice(expected_phrase: str = "Approved phrase") -> bool:
    """
    Authenticate user via voice passphrase.

    Args:
        expected_phrase: The expected passphrase for authentication

    Returns:
        True if voice matches expected phrase, False otherwise
    """
    recognized = recognize_voice()
    if recognized == expected_phrase:
        print("Access granted!")
        return True
    else:
        print(f"Access denied. Heard: {recognized}")
        return False


if __name__ == "__main__":
    # Example usage
    authenticate_voice("Approved phrase")
