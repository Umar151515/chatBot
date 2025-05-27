from utils.image.create_description import create_image_description
from core.config import image_folder_path


class Image:
    def __init__(self, file_name: str, description: str = None):
        self.file_name = file_name
        self.description = description
    
    @property
    def file_path(self) -> str:
        return image_folder_path / (self.file_name + ".png")
    
    async def generate_description(self):
        if not self.description:
            self.description = await create_image_description(str(self.file_path))
        return self.description
    
    def __str__(self):
        return (
            "Image Information:\n"
            f"- Name: {self.file_name}\n"
            f"- Description: {self.description}"
        )