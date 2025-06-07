from aiogram.types import Message

from .image_generation import generate_and_process_image
from .image_variation_create import create_variation_and_process_image
from .send_latex_image import send_and_process_latex_image
from ..messages import edit_message
from core.managers import UserManager
from core.managers import MessagesManager
from utils.text.generator import generate_text
from utils.text.processing import has_latex_math, extract_parts_by_pipe


async def response_generation(user_message: Message):
    user_manager = UserManager()
    messages_manager = MessagesManager()

    user = user_manager.get_user(user_message.from_user.id)

    wait_message = await user_message.reply("⏳ Подождите, идет генерация ответа...")
    
    try:
        generated_text = await generate_text(
            messages_manager.get_messages(user.id, user_message.chat.id), 
            user.text_model, 
            web_search=user.web_search
        )
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

    messages_manager.add_message(
        user.id, 
        wait_message.chat.id,
        "assistant", 
        generated_text,
        wait_message.message_id
    )
    await edit_message(wait_message, f"*{user.text_model}*\n{generated_text}")