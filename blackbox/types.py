from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Optional

class DatabaseType(Enum):
    Asynchronous = "asynchronous"
    Synchronous = "synchronous"
    Universal = "universal"

class DatabaseInterface(ABC):
    def __init__(self, database_type: DatabaseType):
        self.database_type = database_type

    @abstractmethod
    def save_chat(self, chat) -> None:
        pass

    @abstractmethod
    def get_chat(self, chat_id: str):
        pass

    @abstractmethod
    def get_or_create_chat(self, database: 'DatabaseInterface', chat_id: str):
        pass

    @abstractmethod
    def delete_chat(self, chat_id: str) -> None:
        pass

    @abstractmethod
    def get_all_chats(self) -> List:
        pass

    @abstractmethod
    def clear_all_chats(self) -> None:
        pass

    @abstractmethod
    def clear_chat_history(self, chat_id: str) -> None:
        pass

    @abstractmethod
    async def save_chat_async(self, chat) -> None:
        pass

    @abstractmethod
    async def get_chat_async(self, chat_id: str):
        pass

    @abstractmethod
    async def get_or_create_chat_async(self, database: 'DatabaseInterface', chat_id: str):
        pass

    @abstractmethod
    async def delete_chat_async(self, chat_id: str) -> None:
        pass

    @abstractmethod
    async def get_all_chats_async(self) -> List:
        pass

    @abstractmethod
    async def clear_all_chats_async(self) -> None:
        pass

    @abstractmethod
    async def clear_chat_history_async(self, chat_id: str) -> None:
        pass