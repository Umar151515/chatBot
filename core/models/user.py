class User:
    def __init__(
            self,
            id: int,
            requests_limit : int = 5,
            status: str = "limited",
            role_model: str = None,
            text_model: str = None,
            image_model: str = None,
            web_search: bool = False
        ):
        from ..managers import ConfigManager

        self.id = id
        self.requests_limit  = requests_limit 
        self.status = status
        self.role_model = role_model
        self.web_search = web_search

        self.text_model = text_model
        if not text_model:
            self.text_model = ConfigManager.text.selected_model
        self.image_model = image_model
        if not image_model:
            self.image_model = ConfigManager.image.selected_model