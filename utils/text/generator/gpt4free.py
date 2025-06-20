import asyncio

import g4f
import g4f.Provider

from core.managers import ConfigManager
from core.models import Messages
from duckduckgo_search.exceptions import DuckDuckGoSearchException


async def generate_text_gpt4free(
        messages: Messages | list[dict[str, str]] | str, 
        model: str = None, 
        web_search: bool = False,
        waiting_time: int = 60
    ) -> str:

    provider_name = ConfigManager.text.get_tool_config("gpt4free")["selected_provider"]
    provider = getattr(g4f.Provider, provider_name, None)
    client = g4f.AsyncClient(provider=provider)

    if isinstance(messages, list):
        messages = Messages(messages)
    elif isinstance(messages, str):
        messages = Messages([{"role": "user", "content": messages}])
    elif not isinstance(messages, Messages):
        raise ValueError(f"Messages, list[dict[str, str]] or str should be passed and not {type(messages)}")

    if web_search:
        query_messages = messages.get_list(delete_system_role=True) 
        query_messages.append({"role": "system", 
                               "content": ConfigManager.prompts["search_query_generation"]})
        query = await generate_text_gpt4free(query_messages, model)
        tool_calls = [{
            "type": "function",
            "function": {
                "name": "search_tool",
                "arguments": {
                    "query": query,
                    "add_text": True,
                    "timeout": 45
                }
            }
        }]
    else:
        tool_calls = None

    messages = messages.get_list()

    try:
        response = await asyncio.wait_for(client.chat.completions.create(
            model=model if model is not None else ConfigManager.text.get_selected_model("gpt4free"),
            messages=messages,
            temperature=ConfigManager.generation_settings["temperature"],
            max_tokens=ConfigManager.generation_settings["max_tokens"],
            frequency_penalty=ConfigManager.generation_settings["repeat_penalty"],
            stop=ConfigManager.generation_settings["stop_words"],
            tool_calls=tool_calls,
            web_search=False
        ), waiting_time)
    except DuckDuckGoSearchException:
        return await generate_text_gpt4free(messages, model, False, waiting_time)

    return response.choices[0].message.content