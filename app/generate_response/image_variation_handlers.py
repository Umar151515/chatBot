from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models import User

from aiogram.types import Message

from ..utils import edit_message
from .image_processing import process_and_send_image
from utils.image_utils.create_variation import create_variation_gpt4free


async def handle_image_variation(message: Message, user: User, user_text: str, image_name: str, 
                                 prompt_image_generation: str, reply_message:Message = None):
    try:
        await edit_message(message, "🎨✨ Генерация вариации изображения...")
        file_name = await create_variation_gpt4free(prompt_image_generation, 
                                                                 f"data/images/{image_name}.png", user.image_model)
    except Exception as e:
        await edit_message(message, f"{e}\n❌ Произошла ошибка при генерации изображения.", None)
        return
    
    await process_and_send_image(file_name, user, user_text, message, reply_message)