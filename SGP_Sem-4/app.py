from flask import Flask, render_template, request
import speech_recognition as sr
from google_trans_new import google_translator
from gtts import gTTS
import os

app = Flask(__name__)

translator = google_translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    r = sr.Recognizer()

    if request.method == 'POST':
        with sr.Microphone() as source:
            print("Speak now!")
            audio = r.listen(source)
            try:
                speech_text = r.recognize_google(audio)
                print("You said:", speech_text)
                translated_text = translator.translate(speech_text, lang_tgt='fr')
                print("Translated text:", translated_text)

                # Generate output voice
                output_voice = gTTS(translated_text, lang='fr')
                output_voice.save("output_voice.mp3")
                os.system("mpg123 output_voice.mp3")  # Adjust the command based on your system

                return translated_text
            except sr.UnknownValueError:
                print("Could not understand")
                return "Could not understand"
            except sr.RequestError:
                print("Could not request result from Google")
                return "Could not request result from Google"

if __name__ == '__main__':
    app.run(debug=True)
