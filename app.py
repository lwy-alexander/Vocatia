import fasttext
import gradio as gr
import jieba
import requests
import csv
import os
from janome.tokenizer import Tokenizer
from pythainlp.tokenize import word_tokenize as thai_tokenize

model = fasttext.load_model("models/lang_detect.ftz")
jpn_tokenizer = Tokenizer()
GOOGLE_API_KEY = ""

LANG_CODE_TO_NAME = {}
with open("data/raw/langs.txt", encoding="utf-8") as f:
    for line in f:
        if line.strip() and "," in line:
            code, name = line.strip().split(",", 1)
            LANG_CODE_TO_NAME[code.strip()] = name.strip()

def load_language_choices(csv_path="data/raw/google_translate_langs.csv"):
    choices = []
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found.")
        return [("English", "en")]
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                code, name = row[0].strip(), row[1].strip()
                choices.append((name, code))
    return choices

def maybe_tokenize(text):
    contains_cjk = any('\u4e00' <= c <= '\u9fff' for c in text)
    contains_hiragana_katakana = any('\u3040' <= c <= '\u30ff' for c in text)
    contains_thai = any('\u0E00' <= c <= '\u0E7F' for c in text)

    if contains_cjk:
        return " ".join(jieba.lcut(text))
    elif contains_hiragana_katakana:
        return " ".join([t.surface for t in jpn_tokenizer.tokenize(text)])
    elif contains_thai:
        return " ".join(thai_tokenize(text))
    return text

def google_translate_api(text, target_lang, api_key):
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "target": target_lang,
        "format": "text",
        "key": api_key
    }

    response = requests.post(url, data=params)
    if response.status_code == 200:
        result = response.json()
        return result["data"]["translations"][0]["translatedText"]
    else:
        return f"(Translation error: {response.text})"

def detect_and_translate(text, target_lang):
    if not text.strip():
        return "Please enter some text."

    processed = maybe_tokenize(text)
    label, confidence = model.predict(processed)
    lang_code = label[0].replace("__label__", "")
    lang_name = LANG_CODE_TO_NAME.get(lang_code, lang_code)

    result = (
        f"Detected Language: {lang_name} ({lang_code})\n"
        f"Confidence: {confidence[0] * 100:.2f}%\n\n"
    )

    if GOOGLE_API_KEY:
        translated = google_translate_api(text, target_lang, GOOGLE_API_KEY)
        result += f"Translation to {target_lang}:\n{translated}"
    else:
        result += "⚠️ Google Translate API key not set. Skipping translation."

    return result

language_choices = load_language_choices()

iface = gr.Interface(
    fn=detect_and_translate,
    inputs=[
        gr.Textbox(lines=4, placeholder="Enter text here...", label="Input Text"),
        gr.Dropdown(language_choices, label="Translate To"),
    ],
    outputs="text",
    title="Vocatia",
    description="Detects language using fastText, translates using Google Translate API.",
)

if __name__ == "__main__":
    iface.launch()
