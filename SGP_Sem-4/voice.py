from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('voice.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data['text']
    source_lang = data['source_lang']
    target_lang = data['target_lang']
    
    translated_text = translate_text(text, source_lang, target_lang)
    return jsonify({'translated_text': translated_text})

@app.route('/speak')
def speak():
    text = request.args.get('text')
    lang = request.args.get('lang')
    audio = get_audio(text, lang)
    return audio.getvalue(), 200, {'Content-Type': 'audio/mp3'}

def translate_text(text, source_lang, target_lang):
    translator = Translator()
    translated_text = translator.translate(text, src=source_lang, dest=target_lang)
    return translated_text.text

def get_audio(text, lang):
    tts = gTTS(text=text, lang=lang)
    audio = BytesIO()
    tts.write_to_fp(audio)
    audio.seek(0)
    return audio

if __name__ == '__main__':
    app.run(debug=True, port=5003)

