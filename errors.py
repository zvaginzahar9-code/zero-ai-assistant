from aiogram import Router
from aiogram.types import Message
from asgiref.sync import sync_to_async

from core.models import User

router = Router()


async def get_user_obj(user_id):
    return await sync_to_async(
        lambda: User.objects.filter(
            telegram_id=user_id
        ).first()
    )()


# EVERYTHING ELSE
@router.message()
async def unknown_message(message: Message):

    user = await get_user_obj(message.from_user.id)

    language = "ru"

    if user:
        language = user.language

    # UNSUPPORTED CONTENT
    if not message.text:

        if language == "en":
            text = (
                "Unsupported content type.\n"
                "Send text or use menu buttons."
            )
        else:
            text = (
                "Неподдерживаемый тип сообщения.\n"
                "Отправьте текст или используйте кнопки меню."
            )

        await message.answer(text)
        return

    # UNKNOWN COMMAND
    if language == "en":
        text = (
            "Unknown command or message.\n"
            "Use menu buttons."
        )
    else:
        text = (
            "Неизвестная команда или сообщение.\n"
            "Используйте кнопки меню."
        )

    await message.answer(text)