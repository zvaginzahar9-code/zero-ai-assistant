from keyboards import main_menu_keyboard
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.registration_states import Registration
from datetime import datetime

from core.models import User, Activity
from asgiref.sync import sync_to_async

router = Router()


@router.message(Registration.waiting_for_first_name)
async def process_first_name(message: Message, state: FSMContext):

    data = await state.get_data()
    language = data.get("language")

    await state.update_data(first_name=message.text)

    if language == "ru":
        await message.answer("Введите вашу фамилию:")
    else:
        await message.answer("Enter your last name:")

    await state.set_state(Registration.waiting_for_last_name)


@router.message(Registration.waiting_for_last_name)
async def process_last_name(message: Message, state: FSMContext):

    data = await state.get_data()
    language = data.get("language")

    await state.update_data(last_name=message.text)

    if language == "ru":
        await message.answer("Введите дату рождения (ДД.ММ.ГГГГ):")
    else:
        await message.answer("Enter your birth date (DD.MM.YYYY):")

    await state.set_state(Registration.waiting_for_birth_date)


@router.message(Registration.waiting_for_birth_date)
async def process_birth_date(message: Message, state: FSMContext):

    print("SAVE STARTED")

    data = await state.get_data()
    language = data.get("language")

    birth_text = message.text.replace(" ", "").strip()

    try:
        birth_date_obj = datetime.strptime(birth_text, "%d.%m.%Y")

        if birth_date_obj > datetime.now():

            if language == "ru":
                await message.answer("Дата рождения не может быть в будущем.")
            else:
                await message.answer("Birth date cannot be in the future.")

            return

    except ValueError:

        if language == "ru":
            await message.answer("Неверный формат. Введите дату (ДД.ММ.ГГГГ):")
        else:
            await message.answer("Invalid format. Enter date (DD.MM.YYYY):")

        return

    existing_user = await sync_to_async(
        lambda: User.objects.filter(
            telegram_id=message.from_user.id
        ).first()
    )()

    if existing_user:

        print("UPDATING USER")

        existing_user.first_name = data["first_name"]
        existing_user.last_name = data["last_name"]
        existing_user.birth_date = birth_text
        existing_user.language = data["language"]

        await sync_to_async(existing_user.save)()

        print("UPDATED SUCCESS")

    else:

        print("CREATING USER")

        new_user = await sync_to_async(User.objects.create)(
            telegram_id=message.from_user.id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=birth_text,
            language=data["language"]
        )

        print("USER SAVED:", new_user.id)

        all_users = await sync_to_async(list)(User.objects.all())

        print("ALL USERS:", all_users)

    await sync_to_async(Activity.objects.create)(
        telegram_id=message.from_user.id,
        action="User registered"
    )

    if language == "ru":
        await message.answer(
            "Регистрация завершена.\nДобро пожаловать в Zero AI.",
            reply_markup=main_menu_keyboard(language)
        )
    else:
        await message.answer(
            "Registration completed.\nWelcome to Zero AI.",
            reply_markup=main_menu_keyboard(language)
        )

    await state.clear()