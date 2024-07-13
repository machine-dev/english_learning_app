from gtts import gTTS
import os

def speak_word(word):
    tts = gTTS(text=word, lang='en')
    tts.save("word.mp3")
    os.system("mpg321 word.mp3")