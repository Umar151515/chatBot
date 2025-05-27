from __future__ import annotations

import asyncio
from typing import Callable

from core.config import ConfigManager

from .gpt4free import create_image_description_gpt4free
from .ollama import create_image_description_ollama


async def create_image_description(
        image: str | bytes, 
        selected_tool:str = None, 
        max_attempts:int = 3
    ) -> bytes:

    generation_method = selected_tool or ConfigManager.image.selected_tool
    methods: dict[str, Callable[[str | bytes], str]] = {
        "gpt4free": create_image_description_gpt4free,
        "ollama": create_image_description_ollama
    }
    
    for attempt in range(max_attempts):
        await asyncio.sleep(ConfigManager.generation_settings["response_delay"])

        try:
            method = methods.get(generation_method, None)
            if method is None:
                raise TypeError(f"Such a create description tool does not exist: {generation_method}")
            return await method(image)
        except Exception as e:
            if attempt == max_attempts - 1:
                raise RuntimeError(f"All {max_attempts} attempts were unsuccessful") from e