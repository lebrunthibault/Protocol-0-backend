import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()
# sr.Microphone.list_microphone_names()
with mic as source:
    print("starting recording")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    print(audio)
    s = r.recognize_google(audio)
    print(s)
