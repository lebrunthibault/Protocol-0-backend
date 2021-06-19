import logging
from typing import Optional

import speech_recognition as sr

logger = logging.getLogger(__name__)


class SpeechRecognition():
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    async def get_input(self) -> Optional[str]:
        with self.mic as source:
            print("starting recording")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            logger.info("Got audio chunk")
            try:
                return self.recognizer.recognize_google(audio, language="fr-FR")
            except sr.RequestError:
                logger.error("Google SR API unavailable")
            except sr.UnknownValueError:
                logger.error("Unable to recognize speech")

            return None
