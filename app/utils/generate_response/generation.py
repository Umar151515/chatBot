import asyncio

from aiogram.types import Message, BufferedInputFile, InputMediaPhoto

from .image_generation import generate_and_process_image
from .image_variation_create import create_variation_and_process_image
from .send_latex_image import send_and_process_latex_image
from ..messages import edit_message
from core.managers import UserManager
from utils.text.generator import generate_text
from utils.text.processing import has_latex_math, extract_parts_by_pipe


async def response_generation(user_message: Message):
    user = UserManager.get_user(user_message.from_user.id)

    wait_message = await user_message.reply("⏳ Подождите, идет генерация ответа...")
    
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
            await generate_and_process_image(user_message, wait_message, user, keywords[0], keywords[1])
            return
    elif "!create_variation_image" in generated_text:
        keywords = extract_parts_by_pipe(generated_text, "!create_variation_image")
        if len(keywords) != 3:
            generated_text = keywords[0]
        else:
            await create_variation_and_process_image(user_message, wait_message, user, keywords[0], keywords[1], keywords[2])
            return
    elif has_latex_math(generated_text):
        await send_and_process_latex_image(user_message, wait_message, generated_text)
        return

    user.messages.add_message("assistant", generated_text)
    await edit_message(wait_message, f"*{user.text_model}*\n{generated_text}")