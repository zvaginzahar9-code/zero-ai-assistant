import asyncio
import os
import sys
import django

# путь к Django
BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(BASE_DIR, "webapp"))

# настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
django.setup()

# проверка БД 
from django.conf import settings
print("DJANGO DB FILE:", settings.DATABASES['default']['NAME'])

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN


from handlers import start, registration, profile, tasks, activity, support, features, documents

from handlers import errors

async def main():
    print("BOT STARTING...")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(registration.router)
    dp.include_router(profile.router)
    dp.include_router(tasks.router)
    dp.include_router(activity.router)
    dp.include_router(support.router)
    dp.include_router(features.router)
    dp.include_router(documents.router)
    dp.include_router(errors.router) 
    print("BOT STARTED")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())