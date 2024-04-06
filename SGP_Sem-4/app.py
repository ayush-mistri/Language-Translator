from flask import Flask, render_template, request
import pytesseract
from PIL import Image
from googletrans import Translator
from gtts import gTTS
from playsound import playsound

app = Flask(__name__)

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
    tts.save("static/output.mp3")
    playsound("static/output.mp3")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    image_file = request.files['image']
    image_path = "static/uploaded_image.jpg"
    image_file.save(image_path)
    extracted_text = extract_text_from_image(image_path)
    target_language = request.form['target_language']
    translated_text = translate_text(extracted_text, target_language)
    speak_text(translated_text, target_language)
    return render_template('result.html', extracted_text=extracted_text, translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
