from .key_value_base import KeyValueBase
from .paths import generation_settings_config_path




class GenerationSettingsConfig(KeyValueBase):
    config_path = generation_settings_config_path
    _keys = ["temperature", "max_tokens", "repeat_penalty", "response_delay", "stop_words"]