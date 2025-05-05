import uuid

from aiogram import F, Router, Bot
from aiogram.types import Message

from core.logic import UserLogic
from core.models import Image
from config import image_folder_path
from ..utils import edit_message, delete_message
from ..generate_response import handle_bot_response


router = Router()

@router.message(F.photo)
async def photo_processing(message: Message, bot: Bot):
    user = UserLogic.get_user(message.from_user.id)

    try:
        upload_image_message = await message.reply("🖼️ Загрузка изображения...")

        short_id = uuid.uuid4().hex[:6]
        filename = f"{user.id}_{short_id}"

        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file.file_path, image_folder_path / f"{filename}.png")
    except Exception as e:
        await edit_message(upload_image_message, f"{e}\n❌ Произошла ошибка при загрузке изображения.", None)
        return

    try:
        await edit_message(upload_image_message, "🔍 Обработка изображения...")

        image = Image(filename)
        await image.generate_description()
        user.messages.add_image("user", image)
    except Exception as e:
        await edit_message(upload_image_message, f"{e}\n❌ Произошла ошибка при обработке изображения.", parse_mode=None)
        return

    if message.caption:
        user.messages.add_message("user", message.caption)

        await delete_message(upload_image_message)
        await handle_bot_response(message)
    else:
        await edit_message(upload_image_message, "✅ Фото успешно загружено в бота!")