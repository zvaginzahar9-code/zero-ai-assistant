from ai import ask_ai, split_text
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asgiref.sync import sync_to_async

from core.models import User
from keyboards import documents_keyboard, document_ai_keyboard

import pdfplumber
import docx
import os

router = Router()


class DocumentState(StatesGroup):
    waiting_for_document = State()
    waiting_for_question = State()


async def get_user_obj(user_id):
    return await sync_to_async(
        lambda: User.objects.filter(telegram_id=user_id).first()
    )()


# открыть меню документов
@router.message(lambda message: message.text in ["📁 Documents", "📁 Документы"])
async def open_documents(message: Message):

    user = await get_user_obj(message.from_user.id)

    if not user:
        await message.answer("Пользователь не найден.")
        return

    language = user.language

    if language == "en":
        text = "📁 Documents\n\nChoose document type:"
    else:
        text = "📁 Документы\n\nВыберите тип документа:"

    await message.answer(
        text,
        reply_markup=documents_keyboard(language)
    )


# выбор типа документа
@router.message(lambda message: message.text in ["📄 TXT", "📄 PDF", "📄 Word"])
async def choose_document_type(message: Message, state: FSMContext):

    await message.answer("Upload your document")

    await state.set_state(DocumentState.waiting_for_document)


# получение документа
@router.message(DocumentState.waiting_for_document)
async def receive_document(message: Message, state: FSMContext):

    if not message.document:
        await message.answer("Please upload a document file.")
        return

    file = await message.bot.get_file(message.document.file_id)
    file_name = message.document.file_name

    os.makedirs("files", exist_ok=True)
    save_path = f"files/{file_name}"

    await message.bot.download_file(file.file_path, save_path)

    text = ""

    if file_name.endswith(".txt"):
        with open(save_path, "r", encoding="utf-8") as f:
            text = f.read()

    elif file_name.endswith(".pdf"):
        with pdfplumber.open(save_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    elif file_name.endswith(".docx"):
        doc = docx.Document(save_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

    else:
        await message.answer("Unsupported file type.")
        return

    if not text:
        await message.answer("Could not read text from document.")
        return

    await state.update_data(document_text=text)

    user = await get_user_obj(message.from_user.id)
    language = user.language

    if language == "en":
        text_msg = "📄 Document loaded"
    else:
        text_msg = "📄 Документ загружен"

    await message.answer(
        text_msg,
        reply_markup=document_ai_keyboard(language)
    )

    await state.set_state(None)


# SUMMARY
@router.message(lambda message: message.text in ["🧠 Summary", "🧠 Краткое содержание"])
async def document_summary(message: Message, state: FSMContext):

    data = await state.get_data()
    text = data.get("document_text")

    if not text:
        await message.answer("Upload document first")
        return

    await message.answer("AI analyzing document...")

    parts = split_text(text)

    summaries = []

    for part in parts:
        result = ask_ai(
            f"Summarize this part of the document:\n{part}"
        )
        summaries.append(result)

    final = ask_ai(
        f"Combine these summaries into one short summary:\n{summaries}"
    )

    await message.answer(final)


# чат
@router.message(lambda message: message.text in ["❓ Ask question", "❓ Задать вопрос"])
async def ask_question_start(message: Message, state: FSMContext):

    await message.answer(
        "💬 Chat started.\nSend questions.\n/stop to exit."
    )

    await state.set_state(DocumentState.waiting_for_question)


@router.message(DocumentState.waiting_for_question)
async def process_question(message: Message, state: FSMContext):

    if message.text.lower() == "/stop":
        await message.answer("Closed.")
        await state.set_state(None)
        return

    data = await state.get_data()
    text = data.get("document_text")

    if not text:
        await message.answer("Upload document first")
        return

    await message.answer("AI thinking...")

    answer = ask_ai(
        f"Using this document answer:\n{text}\n\nQuestion: {message.text}"
    )

    await message.answer(answer)