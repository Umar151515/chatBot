import sqlite3
from typing import Any

from ..models import User
from ..config import user_data_path


class UserManager:
    _instance: "UserManager" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.create_table()

    def create_table(self):
        with sqlite3.connect(user_data_path) as connect:
            cursor = connect.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    requests_limit  INTEGER DEFAULT 5,
                    status TEXT DEFAULT "limited",
                    role_model TEXT DEFAULT NULL,
                    text_model TEXT,
                    image_model TEXT,
                    web_search BOOLEAN DEFAULT 0
            );""")

    def get_parameters(
        self, 
        user_id: int,
        requests_limit:bool = False, 
        status:bool = False,
        role_model:bool = False,
        text_model:bool = False, 
        image_model:bool = False,
        web_search:bool = False
    ) -> dict[str, Any] | Any:
        
        fields = [field for field, include in {
            "requests_limit": requests_limit,
            "status": status,
            "role_model": role_model,
            "text_model": text_model,
            "image_model": image_model,
            "web_search": web_search
        }.items() if include]

        if not fields:
            raise ValueError("At least one field must be provided to create the user.")
        
        with sqlite3.connect(user_data_path) as connect:
            cursor = connect.cursor()
            cursor.execute(f"SELECT {', '.join(fields)} FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()

        if not row:
            raise ValueError(f"User {user_id} not found.")

        if len(row) > 1:
            return dict(zip(fields, row))
        return row[0]

    def get_user(self, user_id: int, create_user: bool = False) -> User | None:
        with sqlite3.connect(user_data_path) as connect:
            cursor = connect.cursor()

            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(
                    id=user_id,
                    requests_limit=user_data[1],
                    status=user_data[2],
                    role_model=user_data[3],
                    text_model=user_data[4],
                    image_model=user_data[5],
                    web_search=bool(user_data[6])
                )
            elif create_user:
                cursor.execute("INSERT INTO users (user_id) VALUES (?)",
                               (user_id,))
                connect.commit()
                return User(user_id)
            return None

    def create_user(
        self, 
        user_id: int, 
        requests_limit:int = None, 
        status:str = None,
        role_model:str = None,
        text_model:str = None, 
        image_model:str = None,
        web_search:bool = None
    ):
        
        fields_to_update = {
            "user_id": user_id,
            "requests_limit": requests_limit,
            "status": status,
            "role_model": role_model,
            "text_model": text_model,
            "image_model": image_model,
            "web_search": web_search
        }
        fields = {key: value for key, value in fields_to_update.items() if value is not None}
        if not fields:
            raise ValueError("At least one field must be provided to create the user.")

        with sqlite3.connect(user_data_path) as connect:
            cursor = connect.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            if not self.user_exists(user_id):
                columns = ', '.join(fields.keys())
                placeholders = ', '.join(['?'] * len(fields))
                
                cursor.execute(
                    f"INSERT INTO users ({columns}) VALUES ({placeholders})",
                    tuple(fields.values())
                )
                connect.commit()

    def set_user(
        self, 
        user_id: int, 
        requests_limit : int = None, 
        status: str = None, 
        role_model:str = None, 
        text_model: str = None, 
        image_model: str = None,
        web_search: bool = None
    ):
        fields_to_update = {
            "requests_limit": requests_limit,
            "status": status,
            "role_model": role_model,
            "text_model": text_model,
            "image_model": image_model,
            "web_search": web_search
        }
        fields = {key: value for key, value in fields_to_update.items() if value is not None}
        if not fields:
            raise ValueError("At least one field must be provided to update the user.")

        with sqlite3.connect(user_data_path) as connect:
            cursor = connect.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(f"UPDATE users SET {', '.join(f'{key} = ?' for key in fields.keys())} WHERE user_id = ?",
                           (*fields.values(), user_id))

    def user_exists(self, user_id: int) -> bool:
        with sqlite3.connect(user_data_path) as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
            return bool(cursor.fetchone()) is not False