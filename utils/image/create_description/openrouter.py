from __future__ import annotations

import asyncio
import base64

import openai

from core.managers import ConfigManager


async def create_image_description_openrouter(
        image: str | bytes,
        model:str = None,
        waiting_time: int = 120
    ) -> str:

    client = openai.AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=ConfigManager.env["OPENROUTER_API"],
    )

    if not model:
        model = ConfigManager.text.get_tool_config("openrouter")["image_models"][0]

    if isinstance(image, str):
        with open(image, "rb") as image_file:
            image_file = base64.b64encode(image_file.read()).decode("utf-8")
    elif isinstance(image, bytes):
        image_file = base64.b64encode(image).decode("utf-8")
    else:
        raise ValueError("image must be either str (path) or bytes")
    
    completion = await asyncio.wait_for(client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", 
                "content": [ 
                    {
                        "type": "text",
                        "text": ConfigManager.prompts["image_description_guide"]
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_file}"
                        }
                    }
                ]
            }
        ],
        temperature=ConfigManager.generation_settings["temperature"],
        max_tokens=ConfigManager.generation_settings["max_tokens"],
        frequency_penalty=ConfigManager.generation_settings["repeat_penalty"],
        stop=ConfigManager.generation_settings["stop_words"]
    ), waiting_time)

    return completion.choices[0].message.content