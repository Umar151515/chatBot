import markdown
from aiogram.types import Message
from aiogram.enums import ParseMode
from bs4 import BeautifulSoup


async def send_message(
        message: Message, 
        text: str, 
        reply: bool = False, 
        parse_mode: ParseMode = None,
        **kwargs
        ) -> None:

    html = markdown.markdown(text)
    text = "".join(BeautifulSoup(html, "html.parser").find_all(string=True))
    text = text.replace("###", "")

    max_length = 4096
    parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    for part in parts:
        if reply:
            await message.reply(part, parse_mode=parse_mode, **kwargs)
        else:
            await message.answer(part, parse_mode=parse_mode, **kwargs)

async def edit_message(
        message: Message, 
        text: str,
        parse_mode: ParseMode | None = None,
        **kwargs
        ) -> None:
    
    if parse_mode == ParseMode.MARKDOWN:
        parse_mode = ParseMode.HTML
        text = markdown.markdown(text)

    max_length = 4096
    parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    
    await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=parts[0],
            parse_mode=parse_mode,
            **kwargs
        )
    
    for part in parts[1:]:
        await message.answer(part, parse_mode=parse_mode)

async def delete_message(message: Message):
    await message.bot.delete_message(message.chat.id, message.message_id)