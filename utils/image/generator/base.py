import asyncio
from typing import Callable

from core.managers import ConfigManager
from .gpt4free import generate_image_gpt4free


async def generate_image(
        prompt: str, 
        model:str = None, 
        selected_tool:str = None, 
        output_path:str = None,
        max_attempts:int = 3
    ) -> bytes:

    generation_method = selected_tool or ConfigManager.image.selected_tool
    methods = {
        "gpt4free": generate_image_gpt4free
    }
    
    for attempt in range(max_attempts):
        await asyncio.sleep(ConfigManager.generation_settings["response_delay"])

        try:
            method = methods.get(generation_method, None)
            if method is None:
                raise TypeError(f"Such a image generation tool does not exist: {generation_method}")
            return await method(
                prompt=prompt, 
                model=model, 
                output_path=output_path
            )
        except Exception as e:
            if attempt == max_attempts - 1:
                raise RuntimeError(f"All {max_attempts} attempts were unsuccessful") from e