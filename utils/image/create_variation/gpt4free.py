import base64
import asyncio
from io import BytesIO

import g4f
from PIL import Image

from core.managers import ConfigManager


async def create_image_variation_gpt4free(
        prompt: str, 
        input_image: str | bytes, 
        model:str = None, 
        output_path:str = None,
        waiting_time: int = 60
    ) -> bytes:
    
    provider_name = ConfigManager.image.get_tool_config("gpt4free")["selected_provider"]
    provider = getattr(g4f.Provider, provider_name, None)
    client = g4f.AsyncClient(provider=provider)

    if isinstance(input_image, str):
        image_file = open(input_image, "rb")
    elif isinstance(input_image, bytes):
        image_file = BytesIO(input_image)
    else:
        raise ValueError("input_image must be either str (path) or bytes")

    try:
        response = await asyncio.wait_for(client.images.create_variation(
            prompt=prompt,
            image=image_file,
            model=model or ConfigManager.image.get_selected_model("gpt4free"),
        ), waiting_time)
        
        if not response.data or not hasattr(response.data[0], 'b64_json'):
            raise RuntimeError("Unexpected API response format")
            
        base64_data = response.data[0].b64_json
        image_data = base64.b64decode(base64_data)
        
        if output_path:
            with Image.open(BytesIO(image_data)) as img:
                img.save(f"{output_path}.png", format="PNG")

        return image_data
        
    except Exception:
        raise
    finally:
        if isinstance(input_image, str):
            image_file.close()