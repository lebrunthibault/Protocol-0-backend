from sr.recognizer.recognizer import Recognizer
from sr.speech_recognition.speech_recognition import SpeechRecognition


def recognize_speech():
    SpeechRecognition(recognizer=Recognizer())
