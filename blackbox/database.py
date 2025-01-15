from abc import ABC, abstractmethod
from enum import Enum
from blackbox.models import Chat
from typing import List, Dict, Any
from blackbox.types import DatabaseInterface, DatabaseType
from datetime import datetime

class DictDatabase(DatabaseInterface):
    def __init__(self):
        super().__init__(DatabaseType.Universal)
        self.chats: Dict[str, Chat] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}

    def save_chat(self, chat: Chat) -> None:
        self.chats[chat.chat_id] = chat
        self.metadata[chat.chat_id].update({
            'message_count': len(chat.get_messages()),
            'last_updated': datetime.utcnow().isoformat()
        })

    def get_chat(self, chat_id: str) -> Chat:
        return self.chats.get(chat_id)
    
    def get_or_create_chat(self, database: DatabaseInterface, chat_id: str) -> Chat:
        if chat_id not in self.chats:
            self.chats[chat_id] = Chat(database, chat_id)
            self.metadata[chat_id] = {}
        return self.chats[chat_id]
    
    def delete_chat(self, chat_id: str) -> None:
        self.chats.pop(chat_id, None)
        self.metadata.pop(chat_id, None)

    def get_all_chats(self) -> List[Chat]:
        return list(self.chats.values())
    
    def clear_all_chats(self) -> None:
        self.chats.clear()
        self.metadata.clear()

    def clear_chat_history(self, chat_id: str) -> None:
        self.chats[chat_id].clear_history()

    async def save_chat_async(self, chat: Chat) -> None:
        self.chats[chat.chat_id] = chat
        self.metadata[chat.chat_id].update({
            'message_count': len(chat.get_messages()),
            'last_updated': datetime.utcnow().isoformat()
        })

    async def get_chat_async(self, chat_id: str) -> Chat:
        return self.chats.get(chat_id)
    
    async def get_or_create_chat_async(self, database: DatabaseInterface, chat_id: str) -> Chat:
        if chat_id not in self.chats:
            self.chats[chat_id] = Chat(database, chat_id)
            self.metadata[chat_id] = {}
        return self.chats[chat_id]
    
    async def delete_chat_async(self, chat_id: str) -> None:
        self.chats.pop(chat_id, None)
        self.metadata.pop(chat_id, None)

    async def get_all_chats_async(self) -> List[Chat]:
        return list(self.chats.values())
    
    async def clear_all_chats_async(self) -> None:
        self.chats.clear()
        self.metadata.clear()

    async def clear_chat_history_async(self, chat_id: str) -> None:
        self.chats[chat_id].clear_history()





