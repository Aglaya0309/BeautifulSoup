from bs4 import BeautifulSoup
import requests

import requests
from bs4 import BeautifulSoup
from googletrans import Translator

def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        english_word = soup.find("div", id="random_word").text.strip()
        english_definition = soup.find("div", id="random_word_definition").text.strip()

        # Блок перевода
        try:
            translator = Translator(service_urls=['translate.googleapis.com'])
            russian_word = translator.translate(english_word, src='en', dest='ru').text
            russian_definition = translator.translate(english_definition, src='en', dest='ru').text
        except:
            russian_word = english_word + " (перевод недоступен)"
            russian_definition = english_definition + " (перевод недоступен)"

        return {
            "english_word": english_word,
            "russian_word": russian_word,
            "english_definition": english_definition,
            "russian_definition": russian_definition
        }

    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def word_game():
    print("Добро пожаловать в игру!")
    while True:
        word_data = get_english_words()
        if not word_data:
            print("Не удалось загрузить слово. Попробуйте ещё раз.")
            continue

        print(f"Определение: {word_data['russian_definition']}")
        user_guess = input("Угадайте слово: ").strip().lower()
        correct_word = word_data['russian_word'].lower()

        if user_guess == correct_word:
            print("✅ Верно!")
        else:
            print(f"❌ Неверно! Правильное слово: {correct_word}")

        if input("Сыграем ещё? (y/n): ").lower() != 'y':
            print("Спасибо за игру! До свидания!")
            break

word_game()