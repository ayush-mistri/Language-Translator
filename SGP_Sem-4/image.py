from flask import Flask, render_template, request
import pytesseract
from PIL import Image
from googletrans import Translator
from gtts import gTTS
import os
import uuid

app = Flask(__name__, static_folder='static')

# Create folders for storing uploaded images and audio files
uploaded_image_folder = "uploaded_image"
audio_folder = "audio"

if not os.path.exists(os.path.join(app.static_folder, audio_folder)):
    os.makedirs(os.path.join(app.static_folder, audio_folder))

if not os.path.exists(uploaded_image_folder):
    os.makedirs(uploaded_image_folder)

def extract_text_from_image(image_path):
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img)
        return text

def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

def speak_text(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    audio_file = f"{audio_folder}/{uuid.uuid4()}.mp3"  # Generate a unique filename
    tts.save(os.path.join(app.static_folder, audio_file))
    return audio_file

@app.route('/')
def index():
    return render_template('image.html')


@app.route('/home')  # Change the route to avoid conflict
def home():
    return render_template('home.html')

@app.route('/process', methods=['POST'])
def process():
    image_file = request.files['image']
    image_path = f"{uploaded_image_folder}/{uuid.uuid4()}.jpg"
    image_file.save(image_path)
    extracted_text = extract_text_from_image(image_path)
    target_language = request.form['target_language']
    translated_text = translate_text(extracted_text, target_language)
    audio_file = speak_text(translated_text, target_language)
    return render_template('image.html', extracted_text=extracted_text, target_language=target_language, translated_text=translated_text, audio_file=audio_file)

if __name__ == '__main__':
    app.run(debug=True, port=5002)

    