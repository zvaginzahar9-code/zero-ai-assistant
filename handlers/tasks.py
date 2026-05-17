from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asgiref.sync import sync_to_async

from core.models import User, Activity
from keyboards import tasks_keyboard, main_menu_keyboard

router = Router()


class TaskState(StatesGroup):
    waiting_for_task = State()
    waiting_for_delete = State()


# 🔴 МОДЕЛЬ ЗАДАЧИ (если нет — скажи, дам отдельно)
from core.models import Task


# Получение пользователя
async def get_user_obj(user_id):
    return await sync_to_async(
        lambda: User.objects.filter(telegram_id=user_id).first()
    )()


# Открыть меню задач
@router.message(lambda message: message.text in ["📋 Задачи", "📋 Tasks"])
async def open_tasks(message: Message):

    user = await get_user_obj(message.from_user.id)
    language = user.language

    text = "📋 Tasks" if language == "en" else "📋 Задачи"

    await message.answer(
        text,
        reply_markup=tasks_keyboard(language)
    )


# Добавить задачу (старт)
@router.message(lambda message: message.text in ["➕ Add task", "➕ Добавить задачу"])
async def add_task_start(message: Message, state: FSMContext):

    user = await get_user_obj(message.from_user.id)
    language = user.language

    text = "Enter task text:" if language == "en" else "Введите текст задачи:"

    await message.answer(text)
    await state.set_state(TaskState.waiting_for_task)


# Сохранение задачи
@router.message(TaskState.waiting_for_task)
async def save_task(message: Message, state: FSMContext):

    user = await get_user_obj(message.from_user.id)
    language = user.language

    # создаём задачу
    await sync_to_async(Task.objects.create)(
        user=user,
        text=message.text
    )

    await sync_to_async(Activity.objects.create)(
        telegram_id=message.from_user.id,
        action=f"Task added: {message.text}"
    )

    text = "Task added ✔" if language == "en" else "Задача добавлена ✔"

    await message.answer(
        text,
        reply_markup=tasks_keyboard(language)
    )

    await state.clear()


# Показ задач
@router.message(lambda message: message.text in ["📋 My tasks", "📋 Мои задачи"])
async def show_tasks(message: Message):

    user = await get_user_obj(message.from_user.id)
    language = user.language

    tasks = await sync_to_async(
        lambda: list(Task.objects.filter(user=user))
    )()

    if not tasks:
        text = "No tasks yet." if language == "en" else "У вас пока нет задач."
    else:
        text = "📋 Your tasks:\n\n" if language == "en" else "📋 Ваши задачи:\n\n"

        for i, task in enumerate(tasks, start=1):
            text += f"{i}. {task.text}\n"

    await message.answer(
        text,
        reply_markup=tasks_keyboard(language)
    )


# Удаление задачи (начало)
@router.message(lambda message: message.text in ["🗑 Delete task", "🗑 Удалить задачу"])
async def delete_task_start(message: Message, state: FSMContext):

    user = await get_user_obj(message.from_user.id)
    language = user.language

    tasks = await sync_to_async(
        lambda: list(Task.objects.filter(user=user))
    )()

    if not tasks:
        text = "No tasks to delete." if language == "en" else "Нет задач для удаления."
        await message.answer(text)
        return

    text = "Enter task number:\n\n" if language == "en" else "Введите номер:\n\n"

    for i, task in enumerate(tasks, start=1):
        text += f"{i}. {task.text}\n"

    await message.answer(text)
    await state.set_state(TaskState.waiting_for_delete)


# Удаление задачи (процесс)
@router.message(TaskState.waiting_for_delete)
async def delete_task_process(message: Message, state: FSMContext):

    user = await get_user_obj(message.from_user.id)
    language = user.language

    try:
        index = int(message.text) - 1
    except:
        await message.answer("Enter number." if language == "en" else "Введите число.")
        return

    tasks = await sync_to_async(
        lambda: list(Task.objects.filter(user=user))
    )()

    if index < 0 or index >= len(tasks):
        await message.answer("Invalid number." if language == "en" else "Неверный номер.")
        return

    task = tasks[index]

    await sync_to_async(task.delete)()

    await sync_to_async(Activity.objects.create)(
        telegram_id=message.from_user.id,
        action=f"Task deleted: {task.text}"
    )

    text = "Task deleted ✔" if language == "en" else "Задача удалена ✔"

    await message.answer(
        text,
        reply_markup=tasks_keyboard(language)
    )

    await state.clear()


# Назад
@router.message(lambda message: message.text in ["⬅ Back", "⬅ Назад"])
async def back_to_menu(message: Message):

    user = await get_user_obj(message.from_user.id)
    language = user.language

    text = "Main menu" if language == "en" else "Главное меню"

    await message.answer(
        text,
        reply_markup=main_menu_keyboard(language)
    )