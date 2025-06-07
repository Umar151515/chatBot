from aiogram.types import Message, BufferedInputFile, InputMediaPhoto

from ..messages.message_utils import delete_message, edit_message, send_message
from utils.text.convert.text_to_image import latex_to_image_bytes


async def send_and_process_latex_image(user_message: Message, wait_message: Message, latex_text: str):
    try:
        image_bytes_list = latex_to_image_bytes(latex_text)
    
        media = []
        for i, image_bytes in enumerate(image_bytes_list):
            image = BufferedInputFile(
                file=image_bytes,
                filename=f"latex_image_{i}.png"
            )
            media.append(InputMediaPhoto(media=image))
        
        if len(media) == 1:
            await user_message.reply_photo(photo=media[0].media)
        else:
            await user_message.reply_media_group(media=media)

        await delete_message(wait_message)
    except Exception as e:
        await edit_message(wait_message, f"{e}\n❌ Произошла ошибка при создании изображения, сообщение отправлено как текстовый ответ.", None)
        await send_message(user_message, latex_text, True, None)