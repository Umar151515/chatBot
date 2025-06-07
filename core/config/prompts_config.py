from .paths import prompts_config_path
from .key_value_base import KeyValueBase


class PromptsConfig(KeyValueBase):
    config_path = prompts_config_path
    _keys = [
        "search_query_generation",
        "context_internet",
        "image_description_guide",
        "image_generation",
        "create_variation_image",
        "plain_text",
        "math_tagging"
    ]