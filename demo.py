import speech_recognition as s


def take_query():
    sr=s.Recognizer()
    # sr.pause_threshold=3
    print("Say something")
    with s.Microphone() as m:
        try:
            audio = sr.listen(m)
            sr.adjust_for_ambient_noise(m,duration=5)
            text = sr.recognize_google(audio, language="en-in")
            return text
        except:
            print("exception occurred")


print("You said: ",take_query())




