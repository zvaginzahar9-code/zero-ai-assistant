from aiogram import Router
from aiogram.types import Message
from asgiref.sync import sync_to_async

from core.models import User, Activity, Task

router = Router()


async def get_user_obj(user_id):
    return await sync_to_async(
        lambda: User.objects.filter(telegram_id=user_id).first()
    )()


@router.message(lambda message: message.text in ["📊 Activity", "📊 Активность"])
async def show_activity(message: Message):

    user = await get_user_obj(message.from_user.id)

    if not user:
        await message.answer("Пользователь не найден.")
        return

    language = user.language

    tasks = await sync_to_async(
        lambda: list(Task.objects.filter(user=user))
    )()

    activity = await sync_to_async(
        lambda: list(
            Activity.objects
            .filter(telegram_id=user.telegram_id)
            .order_by("-created_at")[:10]
        )
    )()

    tasks_created = len(tasks)

    if language == "en":
        text = "📊 Activity\n\n"
        text += f"Tasks created: {tasks_created}\n\n"
        text += "Recent activity:\n"
    else:
        text = "📊 Активность\n\n"
        text += f"Создано задач: {tasks_created}\n\n"
        text += "Последние действия:\n"

    if not activity:
        text += "No activity." if language == "en" else "Нет действий."
    else:
        for act in activity:
            text += f"{act.created_at.strftime('%d.%m %H:%M')} — {act.action}\n"

    await message.answer(text)