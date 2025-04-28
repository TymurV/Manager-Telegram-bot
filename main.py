from telebot import TeleBot
from config import *
from keyboards import *
from database import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = TeleBot(TOKEN)
support_chat_id = chat_id

init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    telegram_id = message.from_user.id
    username = message.from_user.username or ""
    save_user(telegram_id, username)
    bot.send_message(chat_id, "Добро пожаловать! Выберите опцию:", reply_markup=get_main_menu())

@bot.message_handler(commands=['about'])
def about_project(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Этот бот создан для обучения и развития в сфере IT. Мы предлагаем широкий спектр курсов и материалов, которые помогут вам освоить новые навыки и достичь успеха в IT-сфере.")

@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Если у вас возникли вопросы или проблемы, пожалуйста, свяжитесь с нами через кнопку 'Связаться с нами' в главном меню.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text

    if text == "Курсы":
        bot.send_message(chat_id, "Выберите категорию:", reply_markup=get_categories_menu())
    elif text == "Акция!":
        bot.send_message(chat_id, "Акция! Бесплатный мини курс Python/Java!", reply_markup=get_action_menu())
    elif text == "О нас":
        bot.send_message(chat_id, "Мы - команда профессионалов, которая поможет вам освоить новые навыки и достичь успеха в IT-сфере.")
    elif text == "Связаться с нами":
        bot.send_message(chat_id, "👋 Введите свой вопрос:")
        bot.register_next_step_handler(message, confirm_support_message)
    else:
        bot.send_message(chat_id, "Неверная команда. Пожалуйста, выберите опцию из меню.", reply_markup=get_main_menu())

def confirm_support_message(message):
    chat_id = message.chat.id
    user_data = message.text
    bot.send_message(chat_id, "Отправить сообщение администратору?\nВыберите кнопками ниже", reply_markup=send_message_to_support())
    bot.register_next_step_handler(message, lambda msg: handle_support_message(msg, user_data))

def handle_support_message(message, original_question):
    chat_id = message.chat.id
    text = message.text

    if text == "Отправить ✅":
        user = message.from_user
        user_info = (
            f"📩 Новое сообщение от пользователя:\n"
            f"👤 Имя: {user.first_name or ''} {user.last_name or ''}\n"
            f"🧑‍💻 Username: @{user.username if user.username else 'не указан'}\n"
            f"🆔 ID: {user.id}\n\n"
            f"✉️ Сообщение:\n{original_question}"
        )
        
        # Create reply button
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton("Ответить пользователю", callback_data=f"reply_{user.id}"))
        
        bot.send_message(support_chat_id, user_info, reply_markup=reply_markup)
        bot.send_message(chat_id, "Ваше сообщение отправлено администратору. Ожидайте ответа.", reply_markup=get_main_menu())
    elif text == "Отменить ❌":
        bot.send_message(chat_id, "Отправка сообщения отменена.", reply_markup=get_main_menu())
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите 'Отправить ✅' или 'Отменить ❌'.", reply_markup=send_message_to_support())
        bot.register_next_step_handler(message, lambda msg: handle_support_message(msg, original_question))

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    callback_data = call.data

    try:
        if callback_data.startswith("reply_"):
            user_id = int(callback_data.split("_")[1])
            bot.send_message(chat_id, f"Введите ответ для пользователя (ID: {user_id}):")
            bot.register_next_step_handler(call.message, lambda msg: send_reply_to_user(msg, user_id))
            bot.answer_callback_query(call.id)
            return
            
        if callback_data.startswith("category_"):
            category_id = int(callback_data.split("_")[1])
            bot.send_message(chat_id, "Выберите курс:", reply_markup=get_products_menu(category_id))
            bot.delete_message(chat_id, call.message.message_id)

        elif callback_data.startswith("product_"):
            product_id = int(callback_data.split("_")[1])
            product = get_product(product_id)
            if product:
                name, description, recomended_age, image_path = product
                caption = f"{name}\n\n{description}\nРекомендуемый возраст: {recomended_age}"
                try:
                    with open(image_path, "rb") as photo:
                        bot.send_photo(chat_id, photo, caption=caption, reply_markup=buy_course_button(product_id))
                        bot.delete_message(chat_id, call.message.message_id)
                except FileNotFoundError:
                    bot.send_message(chat_id, f"{caption}\n\nИзображение отсутствует.", reply_markup=buy_course_button(product_id))
                    bot.delete_message(chat_id, call.message.message_id)
            else:
                bot.send_message(chat_id, "Курс не найден.", reply_markup=get_main_menu())

        elif callback_data == "back_to_main_menu":
            bot.send_message(chat_id, "Выберите опцию:", reply_markup=get_main_menu())
            bot.delete_message(chat_id, call.message.message_id)

        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Ошибка в callback_query: {e}")
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте снова.", reply_markup=get_main_menu())
        bot.answer_callback_query(call.id)

def send_reply_to_user(message, user_id):
    admin_reply = message.text
    
    try:
        bot.send_message(user_id, f"📬 Ответ от администратора:\n\n{admin_reply}")
        bot.send_message(message.chat.id, f"✅ Ваш ответ был отправлен пользователю (ID: {user_id})")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Не удалось отправить ответ пользователю: {e}")

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        import time
        time.sleep(5)
