import telebot
import pandas as pd
import pickle
import os
import logging

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models.gigachat import GigaChat
from ultralytics import YOLO
from PIL import Image
from logging.handlers import RotatingFileHandler
from resources.information import translations, template, reply, cont_types
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Настройка логирования

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = RotatingFileHandler('bot.log', maxBytes=1024 * 1024, backupCount=5)
file_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

#Импорт данных

with open('resources/my_dict.pickle', 'rb') as f:
    loaded_dict = pickle.load(f)

df = pd.read_csv("resources/newdf.csv")

# Инициализация GigaChat
txt_token = 'YOUR_TOKEN'
bot_token = 'YOUR_TOKEN'

llm = GigaChat(credentials=txt_token, verify_ssl_certs=False)
conversation = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())
conversation.prompt.template = template

# Запуск бота
bot = telebot.TeleBot(bot_token)

def top_recipes_by_ingredients(ingredient_list, df, num, message):
    user_id = message.chat.id
    recipe_counts = {}

    # Проход по каждой строке датафрейма
    for index, row in df.iterrows():
        # Подсчет количества ингредиентов из списка, входящих в текущий рецепт
        count = sum(ingredient in row['new_clear'] for ingredient in ingredient_list)
        
        # Добавление рецепта и количества вхождений в словарь, сохранение индекса строки
        if count > 0: # Добавляем только рецепты с хотя бы одним совпадением
            recipe_counts[index] = count
    
    # Сортировка словаря по количеству вхождений и выбор индексов топ N рецептов
    top_indices = sorted(recipe_counts, key=recipe_counts.get, reverse=True)[:num]
        
    # Создание итогового словаря для хранения списков деталей топ N рецептов
    top_recipes_lists = {
        'title': [],
        'ingredients': [],
        'instructions': [],
        'image_url': []
    }
        
    recipe_number = 1  # начальное значение номера рецепта

    for idx in top_indices:
        row = df.loc[idx]
        top_recipes_lists['title'].append(row['title'])
        top_recipes_lists['ingredients'].append(row['ingredients'])
        top_recipes_lists['instructions'].append(row['instructions'])
        top_recipes_lists['image_url'].append(row['image_url'])

    recipe_titles = top_recipes_lists['title']
    recipe_ingredients = top_recipes_lists['ingredients']
    recipe_images = top_recipes_lists['image_url']
    for title, ingredients, image_url in zip(recipe_titles, recipe_ingredients, recipe_images):
        recipe_text = f"<b>Рецепт №{recipe_number}</b>\nНазвание: {title}\nИнгредиенты: \n-{ingredients}"
        bot.send_photo(user_id, image_url)
        bot.send_message(user_id, recipe_text, parse_mode="HTML")  # укажите parse_mode="HTML" для разбора HTML-тегов
        recipe_number += 1

    bot.send_message(user_id, "Как тебе рецепты? Понравились?\nДа/Нет")
    bot.register_next_step_handler(message, handle_recipe_feedback, top_recipes_lists, num)

def find_matching_recipes(message, loaded_dict):
    translated_words = []
    for word in message:
        # Если слово есть в словаре, добавляем его значение в новый список
        if word in loaded_dict:
            translated_words += loaded_dict[word]
        # Если слово отсутствует в словаре, добавляем его как есть
        else:
            translated_words.append(word)
    return translated_words

def handle_recipe_feedback(message, top_recipes_lists, num):
    user_id = message.chat.id
    text = message.text.strip().lower()
    user_name = message.from_user.first_name

    if text == 'да':
        bot.send_message(user_id, "Отлично, под каким номером будем готовить рецепт?")
        bot.register_next_step_handler(message, send_recipe_instructions, top_recipes_lists, num)
    elif text == 'нет':
        bot.send_message(user_id, f"Очень жаль, {user_name}. Попробуйте сделать новый текстовый запрос или загрузите фотографию получше, и, возможно, я смогу вам помочь!")
        return
    else:
        bot.send_message(user_id, f"Пожалуйста, {user_name} ,введите 'Да' или 'Нет'. Если ты этого не сделаешь, придется начать все сначала!")
        logger.info(f"Trying to clear step handler for user {user_id} and message {message}")
        bot.clear_step_handler(message)
        logger.info(f"Step handler cleared for user {user_id} and message {message}")
        bot.register_next_step_handler(message, handle_recipe_feedback, top_recipes_lists)

def send_recipe_instructions(message, recipes, num):
    print(f"recipe {recipes}")
    user_id = message.chat.id
    if message.text is not None:  # Проверяем, не является ли message.text None
        text = message.text.strip()
        if not text.isdigit():
            bot.send_message(user_id, "Пожалуйста, введите число.")
            bot.register_next_step_handler(message, send_recipe_instructions, recipes, num)
            return

        recipe_number = int(text)
        if not 1 <= recipe_number <= num:
            bot.send_message(user_id, f"Пожалуйста, выберите номер рецепта от 1 до {num}.")
            bot.register_next_step_handler(message, send_recipe_instructions, recipes, num)
            return

        selected_recipe_index = recipe_number - 1
        selected_recipe_title = recipes['title'][selected_recipe_index]
        selected_recipe_instructions = recipes['instructions'][selected_recipe_index]
        bot.send_message(user_id, f"Рецепт: {selected_recipe_title}\nИнструкции: {selected_recipe_instructions}")
        bot.send_message(user_id, "Надеюсь, вам все понравилось!\nЯ всегда буду рад тебя видеть!")
    else:
        bot.send_message(user_id, f"Извините, но я не могу обработать ваш запрос. Пожалуйста, отправьте цифру от 1 до {num}")

def ask_for_number(message, full_list2):
    user_id = message.chat.id
    num = message.text
    if num.isdigit():
        number = int(num)
        if 1 <= number <= 5:
            full_list3 = find_matching_recipes(full_list2, loaded_dict)
            top_recipes_by_ingredients(full_list3, df, number, message)
        else:
            bot.send_message(user_id, "Пожалуйста, введите число от 1 до 5.")
            # Регистрируем обработчик следующего шага только в случае некорректного ввода
            bot.register_next_step_handler(message, ask_for_number, full_list2)
    else:
        bot.send_message(user_id, "Пожалуйста, введите числовое значение!")
        # Регистрируем обработчик следующего шага только в случае некорректного ввода
        bot.register_next_step_handler(message, ask_for_number, full_list2)

@bot.message_handler(content_types=cont_types)
def not_text(message):
    user_id = message.chat.id
    bot.send_message(user_id, reply)
    logger.info(f"Sticker received from user {user_id}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    text = f'Привет, {user_name}! Введи список продуктов или изображение и я попробую предложить что ты сегодня можешь покушать!\nПредоложи мне желательно продукты, ибо каша из топора может быть только в сказке!'
    bot.send_message(message.chat.id, text)
    logger.info(f'Sent welcome message to user {message.chat.id}')

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    user_id = message.chat.id
    response = conversation.predict(input=message.text)
    if response == "Нет":
        bot.send_message(user_id, "Я что-то не вижу где здесь продукты... Попробуй скорректировать свой запрос!")
    else:
        response = response.lower().split()
        bot.send_message(user_id, f'Скажите, пожалуйста, сколько рецептов Вам рекомендовать?(от 1 до 5)')
        bot.register_next_step_handler(message, ask_for_number, response)
    logger.info(f'Response sent to user {user_id}: {response}')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    model_yolo = YOLO('resources/best.pt')
    user_id = message.chat.id
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot.send_message(user_id, 'Хм... сейчас, присмотрюсь...')
    with open("photo.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    image = Image.open("photo.jpg")
    results = model_yolo.predict(image, conf=0.15)
    
    if not results:
        bot.send_message(user_id, "На фотографии не обнаружены объекты. Пожалуйста, отправьте новую более качественную фотографию или напишите запрос текстом.")
        return
        
    predicted_classes = [model_yolo.names[int(c)] for r in results for c in r.boxes.cls]
    translated_classes = [translations.get(word, word) for word in predicted_classes]
    response_list2 = ' '.join(translated_classes).split()
    full_list2 = find_matching_recipes(response_list2, loaded_dict)
    bot.send_message(user_id, 'Скажите, пожалуйста, сколько рецептов Вам рекомендовать? (от 1 до 5)')
    bot.register_next_step_handler(message, ask_for_number, full_list2)

bot.polling(none_stop=True)

