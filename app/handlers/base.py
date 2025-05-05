from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app import keyboards
from core.models import User
from core.logic import UserLogic
from ..utils import send_message


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    try:
        user = message.from_user

        await send_message(message, f"Привет, *{user.first_name}*!\nЯ бот для общения. Напиши мне что-нибудь, и я отвечу!", 
                     reply_markup=keyboards.get_main_keyboard(UserLogic.get_user(user.id).web_search))
    except Exception as e:
        await send_message(message, f"{e}\n❌ Произошла ошибка при запуске бота. Попробуйте снова.", parse_mode=None)

@router.message(F.text == "👤 Мой аккаунт")
async def enable_web_search(message: Message):
    try:
        user = UserLogic.get_user(message.from_user.id)
        
        account_info = (
            "🔐 <b>Ваш аккаунт</b>\n\n"
            f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
            f"🌟 <b>Статус:</b> {'Полный доступ' if user.full_access else 'Ограниченный'}\n\n"
            "📝 <b>Текстовые модели</b>\n"
            f"• Модель: <code>{user.text_model}</code>\n"
            f"• Инструмент: <code>{user.text_selected_tool}</code>\n\n"
            "🖼️ <b>Изображения</b>\n"
            f"• Модель: <code>{user.image_model}</code>\n"
            f"• Инструмент: <code>{user.image_selected_tool}</code>\n\n"
            f"🔢 <b>Оставшиеся запросы:</b> {user.number_requests}" if not user.full_access else ""
        )

        await send_message(message, account_info, parse_mode=ParseMode.HTML)
    except Exception as e:
        await send_message(message, f"{e}\n❌ Не удалось получить информацию об аккаунте.", parse_mode=None)