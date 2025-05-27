from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models import User

from aiogram.types import Message

from ..messages import edit_message
from .image_processing import process_and_send_image
from utils.image.create_variation import create_image_variation
from utils.file_tools import generate_file_name
from core.config import image_folder_path


async def create_variation_and_process_image(
        user_message: Message,
        wait_message: Message,
        user: User,
        user_content: str,
        image_name: str,
        prompt_image_generation: str,
    ):
    
    try:
        await edit_message(wait_message, "🎨✨ Генерация вариации изображения...")
        file_name = generate_file_name()
        await create_image_variation(
            prompt_image_generation, image_folder_path / f"{image_name}.png",
            user.image_model, output_path=image_folder_path / file_name
        )
    except Exception as e:
        await edit_message(wait_message, f"{e}\n❌ Произошла ошибка при генерации изображения.", None)
        return
    
    await process_and_send_image(file_name, user, user_content, user_message, wait_message)