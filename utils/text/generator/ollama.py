import asyncio

import ollama

from core.managers import ConfigManager
from core.models import Messages
from ..search import duckduckgo_search


async def generate_text_ollama(
        messages: Messages | list[dict[str, str]] | str,
        model:str = "", 
        web_search:bool = False
    ) -> str:

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
        query = await generate_text_ollama(query_messages, model)
        search_results = await duckduckgo_search(query, add_text=True)
        if search_results:
            messages.add_message(
                "system", 
                f"{ConfigManager.prompts['context_internet']}{search_results}"
            )

    messages = messages.get_list()

    response = await asyncio.to_thread(
        ollama.chat,
        model=model or ConfigManager.text.get_selected_model("ollama"),
        messages=messages,
        stream=False,
        options={
            "temperature": ConfigManager.generation_settings["temperature"],
            "num_predict": ConfigManager.generation_settings["max_tokens"],
            "repeat_penalty": ConfigManager.generation_settings["repeat_penalty"],
            "stop": ConfigManager.generation_settings["stop_words"],
        }
    )
    return response['message']['content']