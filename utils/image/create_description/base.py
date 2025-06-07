from __future__ import annotations

import asyncio
from typing import Callable

from core.managers import ConfigManager

from .gpt4free import create_image_description_gpt4free
from .openrouter import create_image_description_openrouter
from .ollama import create_image_description_ollama


async def create_image_description(
        image: str | bytes, 
        selected_tool:str = None, 
        model:str = None,
        max_attempts:int = 3
    ) -> bytes:

    generation_method = selected_tool or ConfigManager.text.selected_tool
    methods = {
        "gpt4free": create_image_description_gpt4free,
        "openrouter": create_image_description_openrouter,
        "ollama": create_image_description_ollama
    }
    
    for attempt in range(max_attempts):
        await asyncio.sleep(ConfigManager.generation_settings["response_delay"])

        try:
            method = methods.get(generation_method, None)
            if method is None:
                raise TypeError(f"Such a create description tool does not exist: {generation_method}")
            return await method(image=image, model=model)
        except Exception as e:
            if attempt == max_attempts - 1:
                raise RuntimeError(f"All {max_attempts} attempts were unsuccessful") from e