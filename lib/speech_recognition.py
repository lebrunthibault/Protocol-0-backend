from typing import Optional

from loguru import logger

import speech_recognition as sr


class SpeechRecognition():
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.1
        self.recognizer.non_speaking_duration = 0.1
        self.recognizer.phrase_threshold = 0.3
        self.mic = sr.Microphone()

    def get_input(self) -> None:
        with self.mic as source:
            logger.info(f"mic info: {self.mic.device_info}")
            logger.info("starting recording")
            # self.recognizer.adjust_for_ambient_noise(source)

            while True:
                audio = self.recognizer.listen(source, phrase_time_limit=3)
                # self._get_words_from_audio(self.recognizer, audio)
        # self.recognizer.listen_in_background(self.mic, self._get_words_from_audio)
        # while True:
        #     pass

    def _get_words_from_audio(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> Optional[str]:
        logger.info(f"Got audio chunk: {audio}")
        try:
            words = recognizer.recognize_google(audio, language="fr-FR", show_all=True)
            # return self.recognizer.recognize_google(audio, language="en-US", show_all=True)
        except sr.RequestError:
            logger.error("Google SR API unavailable")
            return None
        except sr.UnknownValueError:
            logger.error("Unable to recognize speech")
            return None

        if words:
            logger.info(f"got words {words}")
        else:
            logger.info(f"didn't find any thing")

        return None

    # def _listen_for_command(self):
