from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import uuid
from collections import deque
from datetime import datetime
from blackbox.exceptions import DatabaseTypeError
from blackbox.types import DatabaseInterface, DatabaseType


@dataclass
class AgentMode():
    mode: bool
    id: str
    name: str
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "mode": self.mode,
            "id": self.id,
            "name": self.name,
        }
        if self.description:
            data["description"] = self.description
        return data
    
@dataclass
class Model():
    id: str
    name: str
    max_tokens: int
    supports_streaming: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "max_tokens": self.max_tokens,
            "supports_streaming": self.supports_streaming
        }
    
@dataclass
class Message():
    role: str
    content: str
    image: Optional[str] = None
    id: str = None
    timestamp: str = None

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        if self.image:
            return {
                "id": self.id,
                "content": self.content,
                "role": self.role,
                "data": {
                    "fileText": "",
                    "imageBase64": self.image,
                    "title": None,
                }
            }
        return {
            "id": self.id,
            "content": self.content,
            "role": self.role,
        }

@dataclass
class Chat():
    MAX_MESSAGES = 25

    def __init__(self, database: DatabaseInterface, chat_id: str = None):
        self.database = database
        self.chat_id = chat_id or str(uuid.uuid4())
        self.messages = deque(maxlen=self.MAX_MESSAGES)
        self.created_at = datetime.utcnow().isoformat()
        self.metadata = {
            "message_count": 0,
            "last_updated": self.created_at
        }

    def add_message(self, content: str, role: str, image: Optional[str] = None) -> None:
        if self.database.database_type is not DatabaseType.Synchronous and self.database.database_type is not DatabaseType.Universal:
            raise DatabaseTypeError("Synchronous or Universal database type required")
        message = Message(content=content, role=role, image=image)
        self.messages.append(message)
        self.metadata["message_count"] += 1
        self.metadata["last_updated"] = datetime.utcnow().isoformat()
        self.database.save_chat(self)

    async def add_message_async(self, content: str, role: str, image: Optional[str] = None) -> None:
        if self.database.database_type is not DatabaseType.Asynchronous and self.database.database_type is not DatabaseType.Universal:
            raise DatabaseTypeError("Asynchronous or Universal database type required")
        message = Message(content=content, role=role, image=image)
        self.messages.append(message)
        self.metadata["message_count"] += 1
        self.metadata["last_updated"] = datetime.utcnow().isoformat()
        await self.database.save_chat_async(self)

    def get_messages(self) -> List[Message]:
        return self.messages
    
    def clear_history(self) -> None:
        if self.database.database_type is not DatabaseType.Synchronous and self.database.database_type is not DatabaseType.Universal:
            raise DatabaseTypeError("Synchronous or Universal database type required")
        self.messages.clear()
        self.metadata["message_count"] = 0
        self.metadata["last_updated"] = self.created_at
        self.database.save_chat(self)

    async def clear_history_async(self) -> None:
        if self.database.database_type is not DatabaseType.Asynchronous and self.database.database_type is not DatabaseType.Universal:
            raise DatabaseTypeError("Asynchronous or Universal database type required")
        self.messages.clear()
        self.metadata["message_count"] = 0
        self.metadata["last_updated"] = self.created_at
        await self.database.save_chat_async(self)
    
class Models():
    BLACKBOX = Model(
        name="BLACKBOX",
        id="blackbox",
        max_tokens=4096,
        supports_streaming=True
    )

    GPT4 = Model(
        name="GPT-4",
        id="gpt-4o",
        max_tokens=8192,
        supports_streaming=False
    )
