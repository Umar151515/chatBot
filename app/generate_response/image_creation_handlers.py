from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models import User

from aiogram.types import Message

from ..utils import edit_message
from .image_processing import process_and_send_image
from utils.image_utils.generator import generate_image

async def handle_image_creation(message: Message, user: User, user_text: str, 
                       prompt_image_generation: str, reply_message:Message = None):
    try:
        await edit_message(message, "🎨 Генерация изображения...")
        file_name = await generate_image(prompt_image_generation, user.image_model, 
                                                      user.image_selected_tool)
    except Exception as e:
        await edit_message(message, f"{e}\n❌ Произошла ошибка при генерации изображения.", None)
        return
    
    await process_and_send_image(file_name, user, user_text, message, reply_message)