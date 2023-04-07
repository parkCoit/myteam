from gtts import gTTS
from playsound import playsound
import random


class Tts:

    def __init__(self):
        self.text = ''

    @staticmethod
    def run(input_text):
        tts = gTTS(text=input_text, lang="ko")
        title = random.randrange(1, 999999999999999)
        tts.save(f"app/services/chatbot/save/{title}.mp3")
        return playsound(f"app/services/chatbot/save/{title}.mp3")
