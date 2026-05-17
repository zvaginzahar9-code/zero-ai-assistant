from keyboards import main_menu_keyboard, language_keyboard
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from states.registration_states import Registration

# 🔴 Django
from core.models import User, Activity

# 🔴 ВАЖНО
from asgiref.sync import sync_to_async

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):

    user = await sync_to_async(
        lambda: User.objects.filter(
            telegram_id=message.from_user.id
        ).first()
    )()

    if user:
        language = user.language

        if language == "ru":
            text = "Добро пожаловать обратно!"
        else:
            text = "Welcome back!"

        await sync_to_async(Activity.objects.create)(
            telegram_id=message.from_user.id,
            action="Used /start"
        )

        await message.answer(
            text,
            reply_markup=main_menu_keyboard(language)
        )

    else:
        await message.answer(
            "🌐 Choose bot language / Выберите язык",
            reply_markup=language_keyboard()
        )


@router.callback_query(lambda c: c.data.startswith("lang_"))
async def language_selected(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()

    user = await sync_to_async(
        lambda: User.objects.filter(
            telegram_id=callback.from_user.id
        ).first()
    )()

    # язык
    if callback.data == "lang_ru":
        language = "ru"
    else:
        language = "en"

    if user:
        user.language = language
        await sync_to_async(user.save)()

        await sync_to_async(Activity.objects.create)(
            telegram_id=callback.from_user.id,
            action="Changed language"
        )

        if language == "en":
            text = "Language changed successfully."
        else:
            text = "Язык успешно изменён."

        await callback.message.answer(
            text,
            reply_markup=main_menu_keyboard(language)
        )

    else:
        await state.update_data(language=language)

        if language == "en":
            text = "You chose English.\nEnter your name:"
        else:
            text = "Вы выбрали русский.\nВведите ваше имя:"

        await callback.message.answer(text)

        await state.set_state(Registration.waiting_for_first_name)