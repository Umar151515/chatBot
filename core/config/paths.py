from pathlib import Path


config_folder_path = Path("configs")
config_folder_path.mkdir(parents=True, exist_ok=True)

data_folder_path = Path("data")
data_folder_path.mkdir(parents=True, exist_ok=True)

image_folder_path = data_folder_path / "images"
image_folder_path.mkdir(parents=True, exist_ok=True)

env_path = config_folder_path / ".env"
generation_settings_config_path = config_folder_path / "generation_settings.json"
text_generation_config_path = config_folder_path / "text_generation.json"
image_generation_config_path = config_folder_path / "image_generation.json"
prompts_config_path = config_folder_path / "prompts.json"
roles_config_path = config_folder_path / "roles.json"
app_config_path = config_folder_path / "app.json"

user_data_path = data_folder_path / "users.db"
user_data_path.touch(exist_ok=True)

__all__ = [
    'config_folder_path', 
    'env_path', 
    'generation_settings_config_path',
    'text_generation_config_path', 
    'image_generation_config_path',
    'prompts_config_path',
    "roles_config_path",
    "app_config_path",
    'data_folder_path', 
    'image_folder_path', 
    'user_data_path'
]