from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models import User

import os

from aiogram.types import Message, FSInputFile

from core.models import Image
from core.managers import MessagesManager
from ..messages import edit_message, delete_message
from core.config import image_folder_path


async def process_and_send_image(
        image_file_name: str, 
        user: User, 
        user_content: str, 
        user_message: Message,
        wait_message: Message,
        description:str = None
    ):

    messages_manager = MessagesManager()

    try:
        image = Image(image_file_name)
        if description:
            image.description = description
        else:
            image.description = image.generate_description()

        messages_manager.add_message(
            user.id, 
            wait_message.chat.id, 
            "assistant", 
            image
        )
        messages_manager.add_message(
            user.id, 
            wait_message.chat.id,
            "assistant", 
            user_content,
            wait_message.message_id
        )
    except Exception as e:
        os.remove(image_folder_path / (image_file_name + ".png"))
        await edit_message(wait_message, f"{e}\n❌ Произошла ошибка при обработке изображения.", None)
        return

    try:
        await delete_message(wait_message)

        photo=FSInputFile(image.file_path)
        caption=f"🖼️: *{user.image_model}*\n*{user.text_model}*\n{user_content}"
        await user_message.reply_photo(photo, caption)

    except Exception as e:
        os.remove(image.file_path)
        await edit_message(wait_message, f"{e}\n❌ Произошла ошибка при отправке изображения.", None)