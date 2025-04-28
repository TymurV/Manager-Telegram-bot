⸻

Manager-TG-Bot

Бот для покупки курсов в Telegram боте.
⸻

Быстрый старт

Клонирование репозитория

git clone https://github.com/TymurV/Manager-Telegram-bot
cd Manager-TG-Bot

Установка зависимостей

pip install -r requirements.txt

Настройка переменных окружения

Создайте файл .env в корне проекта:

# Пример содержимого .env
TOKEN=ваш_токен
DATABASE=ваша_ссылка_на_базу_данных
images=папка_с_изображениями
chat_id=ваш_chat_id

Запуск проекта

python3 main.py



⸻

Структура проекта

your-project/
├── main.py            # Главный файл проекта
├── keyboards.py    # Кнопки и обработчики
├── database.py       # База данных программы
├── requirements.txt   # Зависимости проекта
├── сonfig.py          # Конфигурация проекта
├── .env               # Переменные окружения
└── README.md          # Документация проекта



⸻

Технологии
 • Python 3.11+
 • Telebot (pyTelegramBotAPI)
 • python-dotenv
 • SQLite3
⸻

Основные команды бота

Команда Описание
/start Приветственное сообщение
/help Помощь
/about Информация о проекте



⸻

Планы по развитию
 • Добавить обработку ошибок
 • Реализовать дополнительные команды
 • Написать тесты
 • Развернуть проект на сервере

⸻

Тестирование

pytest



⸻

Лицензия

Этот проект лицензирован под MIT License.
См. файл LICENSE для подробностей.

⸻

Автор

https://github.com/TymurV

⸻

Связь
 • Telegram: @yourusername (https://t.me/TPI777RCS)

⸻

