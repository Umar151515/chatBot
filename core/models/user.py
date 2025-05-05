from config.manager import ConfigManager


class User:
    def __init__(self, id: int):
        from .messages import Messages
        self.id = id
        self.number_requests = 5
        self.full_access = False
        self.web_search = False

        self.text_selected_tool = ConfigManager.text.selected_tool
        self.text_model = ConfigManager.text.selected_model

        self.image_selected_tool = ConfigManager.image.selected_tool
        self.image_model = ConfigManager.image.selected_model

        self.messages: Messages = Messages()