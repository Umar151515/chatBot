import asyncio, re
from typing import Callable

from core.models import Messages
from core.managers import ConfigManager
from .ollama import generate_text_ollama
from .gpt4free import generate_text_gpt4free
from .openrouter import generate_text_openrouter


async def generate_text(
        messages: Messages | list[dict[str, str]] | str,
        model:str = None, 
        selected_tool:str = None, 
        web_search:bool = False, 
        max_attempts:int = 3
    ) -> str:

    methods = {
        "ollama": generate_text_ollama,
        "gpt4free": generate_text_gpt4free,
        "openrouter": generate_text_openrouter
    }
    generation_method = selected_tool or ConfigManager.text.selected_tool
    
    for attempt in range(max_attempts):
        await asyncio.sleep(ConfigManager.generation_settings["response_delay"])

        try:
            method = methods.get(generation_method, None)
            if method is None:
                raise TypeError(f"Such a text generation tool does not exist: {generation_method}")
            generated_text = await method(
                messages=messages, 
                model=model, 
                web_search=web_search
            )
            if generated_text:
                return generated_text
            raise ValueError("Text generation returned empty value")
        except Exception as e:
            if attempt == max_attempts - 1:
                raise RuntimeError(f"All {max_attempts} attempts were unsuccessful") from e