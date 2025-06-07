import asyncio

import openai

from core.managers import ConfigManager
from core.models import Messages
from ..search import duckduckgo_search


async def generate_text_openrouter(
        messages: Messages | dict[str, str] | str,
        model: str = "", 
        web_search: bool = False,
        waiting_time: int = 60
    ) -> str:
    
    client = openai.AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=ConfigManager.env["OPENROUTER_API"],
    )

    if isinstance(messages, list):
        messages = Messages(messages)
    elif isinstance(messages, str):
        messages = Messages([{"role": "user", "content": messages}])
    elif not isinstance(messages, Messages):
        raise ValueError(f"Messages, list[dict[str, str]] or str should be passed and not {type(messages)}")

    if web_search:
        query_messages = messages.get_list(True) 
        query_messages.append({"role": "system", 
                               "content": ConfigManager.prompts["context_internet"]})
        query = await generate_text_openrouter(query_messages, model)
        search_results = await duckduckgo_search(query, add_text=True)
        if search_results:
            messages.add_message(
                "system", 
                f"{ConfigManager.prompts['context_internet']}{search_results}"
            )

    messages = messages.get_list()

    completion = await asyncio.wait_for(client.chat.completions.create(
        model=model or ConfigManager.text.get_selected_model("openrouter"),
        messages=messages,
        temperature=ConfigManager.generation_settings["temperature"],
        max_tokens=ConfigManager.generation_settings["max_tokens"],
        frequency_penalty=ConfigManager.generation_settings["repeat_penalty"],
        stop=ConfigManager.generation_settings["stop_words"]
    ), waiting_time)

    return completion.choices[0].message.content