from aiogram import Router
from aiogram.types import Message
from asgiref.sync import sync_to_async

from core.models import User

router = Router()


async def get_user_obj(user_id):
    return await sync_to_async(
        lambda: User.objects.filter(telegram_id=user_id).first()
    )()


@router.message(lambda message: message.text in ["🆘 Support", "🆘 Поддержка"])
async def support(message: Message):

    user = await get_user_obj(message.from_user.id)

    if not user:
        await message.answer("Пользователь не найден.")
        return

    language = user.language

    if language == "en":
        text = (
            "🆘 Support\n\n"
            "Contact developer:\n"
            "@Trust7002"
        )
    else:
        text = (
            "🆘 Поддержка\n\n"
            "Связь с разработчиком:\n"
            "@Trust7002"
        )

    await message.answer(text)