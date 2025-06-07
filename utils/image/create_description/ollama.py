from __future__ import annotations

import asyncio

import ollama

from core.managers import ConfigManager


async def create_image_description_ollama(image: str | bytes, model:str = None) -> str:
    if not isinstance(image, (str, bytes)):
        raise ValueError("image must be either str (path) or bytes")
    
    try:
        if not model:
            for model_name in ConfigManager.text.get_models("ollama"):
                model_info = ollama.show(model_name)

                if any("vision" in parametr for parametr in model_info["modelinfo"].keys()):
                    model = model_name
                    break
            else:
                raise RuntimeError("No vision model found in configured Ollama models")

        response = await asyncio.to_thread(
            ollama.chat,
            model=model,
            messages=[{"role": "system", "content": ConfigManager.prompts["image_description_guide"], "images": [image]}],
            stream=False,
            options={
                "temperature": ConfigManager.generation_settings["temperature"],
                "num_predict": ConfigManager.generation_settings["max_tokens"],
                "repeat_penalty": ConfigManager.generation_settings["repeat_penalty"],
                "stop": ConfigManager.generation_settings["stop_words"],
            }
        )

        return response['message']['content']
    except Exception as e:
        raise