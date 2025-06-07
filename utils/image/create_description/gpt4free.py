from __future__ import annotations

import asyncio
from io import BytesIO

import g4f

from core.managers import ConfigManager


async def create_image_description_gpt4free(
        image: str | bytes, 
        model:str = "",
        waiting_time: int = 60
    ) -> str:

    provider_name = ConfigManager.text.get_tool_config("gpt4free")["selected_provider"]
    provider = getattr(g4f.Provider, provider_name, None)
    client = g4f.AsyncClient(provider=provider)

    if isinstance(image, str):
        image_file = open(image, "rb")
    elif isinstance(image, bytes):
        image_file = BytesIO(image)
    else:
        raise ValueError("image must be either str (path) or bytes")
    
    try:
        response = await asyncio.wait_for(client.chat.completions.create(
            messages=[{"role": "user", "content": ConfigManager.prompts["image_description_guide"]}],
            model=model,
            temperature=ConfigManager.generation_settings["temperature"],
            max_tokens=ConfigManager.generation_settings["max_tokens"],
            frequency_penalty=ConfigManager.generation_settings["repeat_penalty"],
            stop=ConfigManager.generation_settings["stop_words"],
            web_search=False,
            image=image_file
        ), waiting_time)

        return response.choices[0].message.content
    
    except Exception as e:
        raise RuntimeError(f"Unexpected error during image description") from e
    finally:
        if isinstance(image, str):
            image_file.close()