from aiogram import Router
from aiogram.types import Message, CallbackQuery

from keyboards import (
    profile_settings_keyboard,
    settings_keyboard,
    language_keyboard,
    main_menu_keyboard
)

from core.models import User
from asgiref.sync import sync_to_async

router = Router()


@router.message(lambda message: message.text in ["👤 Профиль", "👤 Profile"])
async def show_profile(message: Message):

    user = await sync_to_async(
        lambda: User.objects.filter(
            telegram_id=message.from_user.id
        ).first()
    )()

    if not user:
        await message.answer("Профиль не найден.")
        return

    language = user.language

    if language == "en":
        profile_text = (
            f"👤 Profile\n\n"
            f"First name: {user.first_name}\n"
            f"Last name: {user.last_name}\n"
            f"Birth date: {user.birth_date}\n"
            f"Registration date: {user.created_at}"
        )
    else:
        profile_text = (
            f"👤 Профиль\n\n"
            f"Имя: {user.first_name}\n"
            f"Фамилия: {user.last_name}\n"
            f"Дата рождения: {user.birth_date}\n"
            f"Дата регистрации: {user.created_at}"
        )

    await message.answer(
        profile_text,
        reply_markup=profile_settings_keyboard(language)
    )


@router.callback_query(lambda c: c.data == "profile_settings")
async def open_settings(callback: CallbackQuery):

    await callback.message.delete()

    user = await sync_to_async(
        lambda: User.objects.get(
            telegram_id=callback.from_user.id
        )
    )()

    language = user.language

    if language == "en":
        text = "⚙ Settings"
    else:
        text = "⚙ Настройки"

    await callback.message.answer(
        text,
        reply_markup=settings_keyboard(language)
    )


@router.callback_query(lambda c: c.data == "change_language")
async def change_language(callback: CallbackQuery):

    await callback.message.delete()

    await callback.message.answer(
        "🌐 Choose bot language / Выберите язык",
        reply_markup=language_keyboard()
    )


@router.callback_query(lambda c: c.data in ["lang_ru", "lang_en"])
async def new_language_selected(callback: CallbackQuery):

    await callback.message.delete()

    if callback.data == "lang_ru":
        language = "ru"
    else:
        language = "en"

    user = await sync_to_async(
        lambda: User.objects.get(
            telegram_id=callback.from_user.id
        )
    )()

    user.language = language
    await sync_to_async(user.save)()

    if language == "en":
        text = "Language changed."
    else:
        text = "Язык изменён."

    await callback.message.answer(
        text,
        reply_markup=main_menu_keyboard(language)
    )