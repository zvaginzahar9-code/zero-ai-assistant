from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard(language="ru"):

    if language == "en":
        keyboard = [
            [KeyboardButton(text="📋 Tasks"), KeyboardButton(text="📁 Documents")],
            [KeyboardButton(text="📊 Activity"), KeyboardButton(text="👤 Profile")],
            [KeyboardButton(text="ℹ Features"), KeyboardButton(text="🆘 Support")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📋 Задачи"), KeyboardButton(text="📁 Документы")],
            [KeyboardButton(text="📊 Активность"), KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="ℹ Возможности"), KeyboardButton(text="🆘 Поддержка")]
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def language_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
        ]
    )
    return keyboard 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def profile_settings_keyboard(language="ru"):
    if language == "en":
        text = "⚙ Settings"
    else:
        text = "⚙ Настройки"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data="profile_settings")]
        ]
    )


def settings_keyboard(language="ru"):
    if language == "en":
        text = "🌐 Change language"
    else:
        text = "🌐 Сменить язык"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data="change_language")]
        ]
    )
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def tasks_keyboard(language="ru"):

    if language == "en":
        keyboard = [
            [KeyboardButton(text="➕ Add task")],
            [KeyboardButton(text="📋 My tasks")],
            [KeyboardButton(text="🗑 Delete task")],
            [KeyboardButton(text="⬅ Back")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="➕ Добавить задачу")],
            [KeyboardButton(text="📋 Мои задачи")],
            [KeyboardButton(text="🗑 Удалить задачу")],
            [KeyboardButton(text="⬅ Назад")]
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
def documents_keyboard(language="ru"):

    if language == "en":
        keyboard = [
            [KeyboardButton(text="📄 TXT")],
            [KeyboardButton(text="📄 PDF")],
            [KeyboardButton(text="📄 Word")],
            [KeyboardButton(text="⬅ Back")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📄 TXT")],
            [KeyboardButton(text="📄 PDF")],
            [KeyboardButton(text="📄 Word")],
            [KeyboardButton(text="⬅ Назад")]
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def document_ai_keyboard(language="ru"):

    if language == "en":
        keyboard = [
            [KeyboardButton(text="🧠 Summary")],
            [KeyboardButton(text="❓ Ask question")],
            [KeyboardButton(text="⬅ Back")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="🧠 Краткое содержание")],
            [KeyboardButton(text="❓ Задать вопрос")],
            [KeyboardButton(text="⬅ Назад")]
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )