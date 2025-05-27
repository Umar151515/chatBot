from aiogram import F, Router
from aiogram.types import Message

from core.managers import UserManager
from ..utils.messages import send_message
from ..utils.generate_response import response_generation


router = Router()

@router.message(F.text == "🗑️ Очистить чат")
async def clear_chat(message: Message):
    try:
        user = UserManager.get_user(message.from_user.id)
        user.messages.clear_messages()

        await send_message(message, f"🧹Чат очищен")
    except Exception as e:
        await send_message(message, f"{e}\n❌ Не удалось очистить чат.", parse_mode=None)


@router.message(F.text == "🔍 История чата")
async def chat_history(message: Message):
    try:
        messages = UserManager.get_user(message.from_user.id).messages.messages
        messages_text = ""

        for message_dict in messages:
            messages_text += f"{message_dict["role"]}: {message_dict["content"]}\n\n"

        await send_message(message, messages_text, parse_mode=None)
    except Exception as e:
        await send_message(message, f"{e}\n❌ Не удалось отправить историю чата.", parse_mode=None)


@router.message(F.text)
async def handle_text_message(message: Message):
    try:
        user = UserManager.get_user(message.from_user.id)
        user.messages.add_message("user", message.text)

        await response_generation(message)
    except Exception as e:
        await send_message(message, f"{e}\n❌ Произошла ошибка при генерации ответа.", True, None)