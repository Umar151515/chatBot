from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models import User

import os

from aiogram.types import Message, FSInputFile

from core.models import Image
from ..utils import edit_message, delete_message
from config import image_folder_path


async def process_and_send_image(file_name: str, user: User, user_text: str, 
                           message: Message, reply_message:Message = None):
    try:
        image = Image(file_name)
        await image.generate_description()

        user.messages.add_image("assistant", image)
        user.messages.add_message("assistant", user_text)
    except Exception as e:
        os.remove(image_folder_path / (file_name + ".png"))
        await edit_message(message, f"{e}\n❌ Произошла ошибка при обработке изображения.", None)
        return

    try:
        await delete_message(message)

        photo=FSInputFile(image.file_path)
        caption=f"🖼️: {user.image_model}\n{user.text_model}\n{user_text}"
        if reply_message:
            await reply_message.reply_photo(photo, caption)
        else:
            await message.answer_photo(photo, caption)

    except Exception as e:
        os.remove(image.file_path)
        await edit_message(message, f"{e}\n❌ Произошла ошибка при отправке изображения.", None)