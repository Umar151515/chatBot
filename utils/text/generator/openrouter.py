import openai

from core.config import ConfigManager
from core.models import Messages
from ..search import duckduckgo_search


async def generate_text_openrouter(messages: Messages, model: str = "", web_search: bool = False) -> str:
    client = openai.AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=ConfigManager.env["OPENROUTER_API"],
    )

    if web_search:
        query_messages = messages.get_messages()
        query_messages.add_message("system", ConfigManager.prompts["context_internet"])
        query = await generate_text_openrouter(query_messages, model)
        search_results = await duckduckgo_search(query, add_text=True)
        if search_results:
            messages.add_message("system", f"{ConfigManager.prompts['context_internet']}{search_results}")

    completion = await client.chat.completions.create(
        model=model or ConfigManager.text.get_selected_model("openrouter"),
        messages=messages.messages,
        temperature=ConfigManager.generation_settings["temperature"],
        max_tokens=ConfigManager.generation_settings["max_tokens"],
        frequency_penalty=ConfigManager.generation_settings["repeat_penalty"],
        stop=ConfigManager.generation_settings["stop_words"]
    )

    return completion.choices[0].message.content