import pytesseract
from PIL import Image
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound

def extract_text_from_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
        return text

def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

def speak_text(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("output.mp3")
    playsound("output.mp3")  # This will play the MP3 file

# Example usage
image_path = input("Enter the path to the image: ")
extracted_text = extract_text_from_image(image_path)
print("Extracted Text:")
print(extracted_text)

target_language = input("Enter the target language (e.g., 'gu' for Gujarati): ")
translated_text = translate_text(extracted_text, target_language)
print("\nTranslated Text:")
print(translated_text)

speak_text(translated_text, target_language)
