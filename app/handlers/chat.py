from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

from core.models import User
from core.logic import UserLogic
from ..utils import send_message
from ..generate_response import handle_bot_response


router = Router()

@router.message(F.text == "🗑️ Очистить чат")
async def clear_chat(message: Message):
    try:
        user = UserLogic.get_user(message.from_user.id)
        user.messages.clear_messages()

        await send_message(message, f"🧹Чат очищен")
    except Exception as e:
        await send_message(message, f"{e}\n❌ Не удалось очистить чат.", parse_mode=None)


@router.message(F.text == "🔍 История чата")
async def chat_history(message: Message):
    try:
        messages = UserLogic.get_user(message.from_user.id).messages.messages
        messages_text = ""

        for message_dict in messages:
            messages_text += f"{message_dict["role"]}: {message_dict["content"]}\n\n"

        await send_message(message, messages_text, parse_mode=None)
    except Exception as e:
        await send_message(message, f"{e}\n❌ Не удалось отправить историю чата.", parse_mode=None)


@router.message(F.text)
async def handle_text_message(message: Message):
    try:
        user = UserLogic.get_user(message.from_user.id)
        user.messages.add_message("user", message.text)

        await handle_bot_response(message)
    except Exception as e:
        await send_message(message, f"{e}\n❌ Произошла ошибка при генерации ответа.", True, None)