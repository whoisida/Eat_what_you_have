# Ешь, что дали!       
### Основная идея проекта:<br>
### TelegramBot **https://t.me/chooserecipebot**


Это инновационный Telegram-бот, разработанный с целью помочь пользователю подобрать рецепты из тех продуктов, которые есть у него буквально на полке в холодильнике.

 - парсинг 1500 c [сайта](https://www.say7.info) рецептов при помощи библиотеки BeautifulSoup

 - предобработка и структурирование текстовых данных с помощью NLP библиотки nltk

 - размечено 3838 фотографий [dataset](https://app.roboflow.com/foods-project) на 113 классов продуктов при помощи Roboflow
   
 - работа с дисбалансом классов изображений для обучения модели детекции YOLO-8 (уменьшение мажориторных классов, увеличение миноритарных классов)
   
 - создана структура подбора рецепта из предпочтений пользователя,а также возможность диалога с ботом с оценкой пользователем работы бота
   
 - дообучена [модель](https://huggingface.co/cointegrated/rubert-tiny2) ruBERT-tiny2 (SentensTransformers)
   
 - использована [модель](https://developers.sber.ru/gigachat/login?ysclid=lthb8b07w5358928848) GigaChat для предобработки пользовательского запроса

 - это все работает в телеграм боте(библиотека telebot)
  
 - запущено на ВМ Selectel

 - наш стэк

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org) [![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org) [![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org) 
 [![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)](#)
 [![Git](https://img.shields.io/badge/Git-%23F05032.svg?style=for-the-badge&logo=Git&logoColor=white)](https://git-scm.com/)
 [![Google Colab](https://img.shields.io/badge/Google_Colab-F9AB00?style=for-the-badge&logo=google-colab&logoColor=white)](https://colab.research.google.com/)
 [![YOLO](https://img.shields.io/badge/YOLO-%23F37626.svg?style=for-the-badge&logo=YOLO&logoColor=white)](https://github.com/AlexeyAB/darknet)
 [![Detectron2](https://img.shields.io/badge/Detectron2-%231A1A1A.svg?style=for-the-badge&logo=Detectron2&logoColor=white)](https://github.com/facebookresearch/detectron2)
 [![Roboflow](https://img.shields.io/badge/Roboflow-%23FF6B6B.svg?style=for-the-badge&logo=Roboflow&logoColor=white)](https://roboflow.com/)
 [![Hugging Face](https://img.shields.io/badge/Hugging%20Face-%23FFD700.svg?style=for-the-badge&logo=Hugging%20Face&logoColor=black)](https://huggingface.co/)
[![Telebot](https://img.shields.io/badge/Telebot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://github.com/eternnoir/pyTelegramBotAPI)
[![gigachat](https://img.shields.io/badge/gigachat-2CA5E0?style=for-the-badge)](https://gigachat.io/)

*Выпускной проект |  ELBRUS Bootcamp*

## Над проектом работали:<br>
[Константин Салафонов](https://github.com/sakoser)<br>
[Оксана Шаталова](https://github.com/datascientist23)<br>
[Ида Климанова](https://github.com/whoisida)<br>
