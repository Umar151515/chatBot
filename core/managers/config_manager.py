from ..config import (
    EnvManager,
    GenerationSettingsConfig,
    PromptsConfig,
    TextGenerationConfig,
    ImageGenerationConfig,
    RolesConfig,
    AppConfig
)


class ConfigManager:
    env: EnvManager = EnvManager()
    generation_settings: GenerationSettingsConfig = GenerationSettingsConfig()
    prompts: PromptsConfig = PromptsConfig()
    text: TextGenerationConfig = TextGenerationConfig()
    image: ImageGenerationConfig = ImageGenerationConfig()
    roles: RolesConfig = RolesConfig()
    app: AppConfig = AppConfig()

    @classmethod
    def reload_all(cls):
        cls.env = EnvManager()
        cls.generation_settings = GenerationSettingsConfig()
        cls.prompts = PromptsConfig()
        cls.text = TextGenerationConfig()
        cls.image = ImageGenerationConfig()
        cls.roles = RolesConfig()
        cls.app = AppConfig()