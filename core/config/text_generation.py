from g4f import Provider
from ollama import list as ollama_models

from .paths import text_generation_config_path
from .generation_config_base import GenerationConfigBase


class TextGeneration(GenerationConfigBase):
    config_path = text_generation_config_path
    _tools = ["gpt4free", "ollama", "openrouter"]
    _gpt4free_models = [
        "claude-2",
        "claude-3",
        "deepseek-r1",
        "deepseek-v2",
        "deepseek-v3",
        "gemini-1.5-pro",
        "gemini-2.0-flash",
        "gemini-2.0-flash-thinking",
        "gemini-pro",
        "gemini-ultra",
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4.1-nano",
        "gpt-4.5",
        "gpt-4.5-preview",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "grok-3",
        "grok-3-r1",
        "llama-3-70b",
        "o1",
        "o3",
        "o3-mini",
        "o4-mini",
        "palm-2",
        "phi-3"
    ]

    def additional_config_customization(self):
        gpt4free = self.get_tool_config("gpt4free")

        if "providers" not in gpt4free or "selected_provider" not in gpt4free:
            gpt4free["providers"] = []
            gpt4free["selected_provider"] = ""
            self.save()
            raise ValueError(
                "Two important parameters ('providers' and 'selected_provider') were not found in gpt4free configuration. "
                "They have been initialized with empty values. Please fill these parameters before running again:\n"
                "- 'providers' should be a list of available providers\n"
                "- 'selected_provider' should be the currently selected provider from the list"
            )
        
        if gpt4free["selected_provider"] == "auto":
            gpt4free["models"] = self._gpt4free_models
        else:
            selected_provider = getattr(Provider, gpt4free["selected_provider"], None)
            if selected_provider is None:
                raise ValueError("text selected_provider is not set")
            provider_models = selected_provider.get_models()
            gpt4free["models"] = sorted(list(set(provider_models) & set(self._gpt4free_models)))
        
        if gpt4free["selected_model"] not in gpt4free["models"] and gpt4free["models"]:
            gpt4free["selected_model"] = gpt4free["models"][0]

        ollama = self.get_tool_config("ollama")
        ollama["models"] = [model.model for model in ollama_models()['models']]
        if ollama["selected_model"] not in ollama["models"] and ollama["models"]:
            ollama["selected_model"] = ollama["models"][0]

        self.save()