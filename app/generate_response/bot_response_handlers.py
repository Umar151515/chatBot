import asyncio

from aiogram.types import Message, BufferedInputFile, InputMediaPhoto

from .image_creation_handlers import handle_image_creation
from .image_variation_handlers import handle_image_variation
from ..utils import edit_message, delete_message, send_message
from core.logic import UserLogic
from utils.text_utils.generator import generate_text
from utils.text_utils.convert.text_to_image import latex_to_image_bytes
from utils.text_utils.processing import has_latex_math, extract_parts_by_pipe


async def safe_generate_text_with_retry(*args, timeout=60, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        task = asyncio.create_task(generate_text(*args, **kwargs))
        try:
            return await asyncio.wait_for(task, timeout=timeout)
        except asyncio.TimeoutError:
            print(f"Попытка {attempt + 1}: таймаут. Отменяю задачу...")
            task.cancel()
            try:
                await task  # дать шанс корректно завершиться
            except asyncio.CancelledError:
                print("Задача успешно отменена.")
            continue
    raise TimeoutError(f"Функция не завершилась за {timeout} секунд после {max_retries} попыток.")


async def handle_bot_response(message: Message):
    user = UserLogic.get_user(message.from_user.id)

    wait_message = await message.reply("⏳ Подождите, идет генерация ответа...")
    
    try:
        generated_text = await generate_text(user.messages, user.text_model, 
                                                         user.text_selected_tool, user.web_search)
    except Exception as e:
        await edit_message(wait_message, f"{e}\n❌ Произошла ошибка при генерации текста.", None)
        return

    if "!create_image" in generated_text:
        keywords = extract_parts_by_pipe(generated_text, "!create_image")
        if len(keywords) != 2:
            generated_text = keywords[0]
        else:
            await handle_image_creation(wait_message, user, keywords[0], keywords[1], message)
            return
    elif "!create_variation_image" in generated_text:
        keywords = extract_parts_by_pipe(generated_text, "!create_variation_image")
        if len(keywords) != 3:
            generated_text = keywords[0]
        else:
            await handle_image_variation(wait_message, user, keywords[0], keywords[1], keywords[2], message)
            return

    elif has_latex_math(generated_text):
        try:
            image_bytes_list = latex_to_image_bytes(generated_text)
        
            media = []
            for i, img_bytes in enumerate(image_bytes_list):
                file = BufferedInputFile(
                    file=img_bytes,
                    filename=f"latex_image_{i}.png"
                )
                if i == 0:
                    media.append(InputMediaPhoto(media=file, caption="Результат LaTeX"))
                else:
                    media.append(InputMediaPhoto(media=file))
            
            if len(media) == 1:
                await message.answer_photo(photo=media[0].media, caption=media[0].caption)
            else:
                await message.answer_media_group(media=media)

            await delete_message(wait_message)

            return
        except Exception as e:
            await send_message(wait_message, f"{e}\n❌ Произошла ошибка при создании изображения, сообщение отправлено как текстовый ответ.", None)

    user.messages.add_message("assistant", generated_text)
    await edit_message(wait_message, f"{user.text_model}\n{generated_text}")