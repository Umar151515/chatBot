from .paths import roles_config_path
from .key_value_base import KeyValueBase


class Roles(KeyValueBase):
    config_path = roles_config_path
    _keys = []