# Vocatia

Vocatia is an AI based language identifier with the addition of Google Translate API to translate the language. Vocatia used the language data from Tatoeba and trained with fastText model to identify the language.
What are in this website:
- Language identifier which can identify 100+ different languages.
- Language translation to 100+ different languages.

---

How to run it:
1. Download all resources, including data.zip and model.zip in the Google Drive.
2. Download all the requirements.txt libraries.
3. Make a project folder with this structure:
|- Vocatia/
  |- data/
    |- raw/
      |- google_translate_langs.csv
      |- langs.txt
      |- sentences.txt
  |- model/
    |-lang_detect.ftz
  |- app.py
  |- script.ipynb
4. [Opsional] Run the script.ipynb (if you want to make new model).
5. [Opsional] Get Google Translate API key and put it on the app.py
6. Run app.py

---

The project made by:
- Helen Febriyanto
- Leonardo Alexander Wijaya
- Lynel Angelica Madelyn
- Olivia The

Hugging Face deployment:
https://huggingface.co/spaces/lynelam/Vocatia_AI

Resources of the project:
https://drive.google.com/drive/folders/1NxYRlF0VAAQJjFGNQGBG3zAlkDW-EaGp?usp=drive_link
