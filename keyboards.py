from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_categories, get_products

def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Курсы"))
    markup.add(KeyboardButton("Акция!"))
    markup.add(KeyboardButton("О нас"))
    markup.add(KeyboardButton("Связаться с нами"))
    return markup

def get_categories_menu():
    categories = get_categories()
    markup = InlineKeyboardMarkup()
    for cat_id, name in categories:
        markup.add(InlineKeyboardButton(name, callback_data=f"category_{cat_id}"))
    return markup

def get_action_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🛒 Купить", url="https://google.com"))
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="back_to_main_menu"))
    return markup

def get_products_menu(category_id):
    products = get_products(category_id)
    markup = InlineKeyboardMarkup()
    for prod_id, name in products:
        markup.add(InlineKeyboardButton(name, callback_data=f"product_{prod_id}"))
    return markup

def get_back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return markup

def buy_course_button(product_id):
    markup = InlineKeyboardMarkup()
    buy_button = InlineKeyboardButton(text="🛒 Купить", url="https://google.com")
    back_button = InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main_menu")
    markup.add(buy_button)
    markup.add(back_button)
    return markup

def send_message_to_support():
    markup =  ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Отменить ❌"))
    markup.add(KeyboardButton("Отправить ✅"))
    return markup