from g4f import Provider

from .paths import image_generation_config_path
from .generation_config_base import GenerationConfigBase


class ImageGeneration(GenerationConfigBase):
    config_path = image_generation_config_path
    _gpt4free_models = {"dall-e-3", "midjourney", "flux", "flux-pro"}
    _tools = ["gpt4free"]

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
                raise ValueError("image selected_provider is not set")
            provider_models = selected_provider.get_models()
            gpt4free["models"] = sorted(list(set(provider_models) & set(self._gpt4free_models)))
        
        if gpt4free["selected_model"] not in gpt4free["models"] and gpt4free["models"]:
            gpt4free["selected_model"] = gpt4free["models"][0]

        self.save()