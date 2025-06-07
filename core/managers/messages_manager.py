from __future__ import annotations

import sqlite3

from ..models.image import Image
from ..models.messages import Messages
from ..config import user_data_path
from ..config import image_folder_path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass


class MessagesManager:
    _instance: "MessagesManager" = None

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
                CREATE TABLE IF NOT EXISTS messages (
                    user_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER,
                           
                    role TEXT NOT NULL,

                    content TEXT,
                    file_name TEXT,

                    type TEXT NOT NULL,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );""")

    def add_message(
        self, 
        user_id: int, 
        chat_id: int,  
        role: str, 
        content: str | Image,
        message_id:int = None,
    ) -> None:
        
        with sqlite3.connect(user_data_path) as connect:
            cursor = connect.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            if isinstance(content, Image):
                file_name = content.file_name
                content = content.description
                cursor.execute("INSERT INTO messages (user_id, chat_id, message_id, role, content, file_name, type) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (user_id, chat_id, message_id, role, content, file_name, "image"))
            elif isinstance(content, str):
                cursor.execute("INSERT INTO messages (user_id, chat_id, message_id, role, content, type) VALUES (?, ?, ?, ?, ?, ?)",
                               (user_id, chat_id, message_id, role, content, "text"))
            else:
                raise ValueError("Content must be either a string or an Image instance.")

    def get_messages(
        self,
        user_id:int = None,
        chat_id:int = None,
        id:int = None,
        message_id:int = None,
        limit:int = None
    ) -> Messages:
        query = """
            SELECT role, content, file_name, type 
            FROM messages 
            WHERE 1=1
        """
        params = []
        
        
        if id is not None:
            query += " AND id = ?"
            params.append(id)
        if user_id is not None:
            query += " AND user_id = ?"
            params.append(user_id)
        if chat_id is not None:
            query += " AND chat_id = ?"
            params.append(chat_id)
        if message_id is not None:
            query += " AND message_id = ?"
            params.append(message_id)

        query += " ORDER BY created_at ASC"
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)

        with sqlite3.connect(user_data_path) as connect:
            cursor = connect.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query, params)
            rows = cursor.fetchall()
        
        messages = []
        for role, content, file_name, type_ in rows:
            if type_ == "text":
                messages.append({"role": role, "content": content})
            elif type_ == "image":
                messages.append({"role": role, "content": Image(file_name, content)})
        
        return Messages(messages)
    
    def clear_messages(
        self,
        user_id: int = None,
        chat_id: int = None,
        id: int = None,
        message_id: int = None
    ) -> None:
        query = "SELECT file_name FROM messages WHERE type = 'image'"
        params = []
        conditions = []
        
        if id is not None:
            conditions.append("id = ?")
            params.append(id)
        if user_id is not None:
            conditions.append("user_id = ?")
            params.append(user_id)
        if chat_id is not None:
            conditions.append("chat_id = ?")
            params.append(chat_id)
        if message_id is not None:
            conditions.append("message_id = ?")
            params.append(message_id)
        
        if conditions:
            query += " AND " + " AND ".join(conditions)

        with sqlite3.connect(user_data_path) as connect:
            cursor = connect.cursor()
            
            cursor.execute(query, params)
            images = [row[0] for row in cursor.fetchall() if row[0]]
            
            delete_query = "DELETE FROM messages"
            if conditions:
                delete_query += " WHERE " + " AND ".join(conditions)
            cursor.execute(delete_query, params)
            connect.commit()

        for file_name in images:
            if not file_name:
                continue
                
            file_path = image_folder_path / f"{file_name}.png"
            try:
                if file_path.exists():
                    file_path.unlink()
            except:
                continue

    def set_system_prompt(self, user_id:int = None, chat_id:int = None, role_model:str = None):
        from . import ConfigManager
        if role_model:
            self.add_message(user_id, chat_id, "system", ConfigManager.roles[role_model])
        self.add_message(user_id, chat_id, "system", ConfigManager.prompts["language"])
        self.add_message(user_id, chat_id, "system", ConfigManager.prompts["image_generation"])
        self.add_message(user_id, chat_id, "system", ConfigManager.prompts["create_variation_image"])
        self.add_message(user_id, chat_id, "system", ConfigManager.prompts["image_metadata_prompt"])