from aiogram import Router
from aiogram.types import Message
from asgiref.sync import sync_to_async

from core.models import User

router = Router()


async def get_user_obj(user_id):
    return await sync_to_async(
        lambda: User.objects.filter(telegram_id=user_id).first()
    )()


@router.message(lambda message: message.text in ["ℹ Features", "ℹ Возможности"])
async def show_features(message: Message):

    user = await get_user_obj(message.from_user.id)
    language = user.language

    if language == "en":
        text = "ℹ Features\n\nTask manager, Activity, Profile, AI"
    else:
        text = "ℹ Возможности\n\nЗадачи, Активность, Профиль, AI"

    await message.answer(text)