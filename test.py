from blackbox.cookies import CookieManager
from blackbox.image import ImageTool
from blackbox.client import AIClient
from blackbox.models import Models
import asyncio
from blackbox.types import DatabaseInterface, DatabaseType
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete
from blackbox.models import Chat
from sqlalchemy.orm import declarative_base
from sqlalchemy import select
from typing import List
from sqlalchemy import Column, String, JSON
from test_models import Base, ChatModel

class AsyncSQLiteDatabase(DatabaseInterface):
    def __init__(self):
        super().__init__(DatabaseType.Asynchronous)
        self.engine = create_async_engine("sqlite+aiosqlite:///test.db")
        self.session = sessionmaker(self.engine, class_=AsyncSession)
        self.Base = Base
        asyncio.create_task(self._create_tables())

    def save_chat(self, chat: Chat) -> None:
        raise NotImplementedError("Asynchronous database does not support saving chats")
    
    def get_chat(self, chat_id: str) -> Chat:
        raise NotImplementedError("Asynchronous database does not support getting chats")
    
    def delete_chat(self, chat_id: str) -> None:
        raise NotImplementedError("Asynchronous database does not support deleting chats")
    
    def get_all_chats(self) -> List[Chat]:
        raise NotImplementedError("Asynchronous database does not support getting all chats")
    
    def clear_chat_history(self, chat_id: str) -> None:
        raise NotImplementedError("Asynchronous database does not support clearing chat history")
    
    def clear_all_chats(self) -> None:
        raise NotImplementedError("Asynchronous database does not support clearing all chats")

    def get_or_create_chat(self, chat_id: str) -> Chat:
        raise NotImplementedError("Asynchronous database does not support getting or creating chats")

    async def _create_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def save_chat_async(self, chat: Chat) -> None:
        async with self.session() as session:
            chat_model = ChatModel.from_chat(chat)
            async with session.begin():
                # Пробуем найти существующую запись
                existing = await session.get(ChatModel, chat.chat_id)
                if existing:
                    # Обновляем существующую запись
                    existing.created_at = chat_model.created_at
                    existing.chat_metadata = chat_model.chat_metadata
                    existing.messages = chat_model.messages
                else:
                    # Создаем новую запись
                    session.add(chat_model)

    async def get_chat_async(self, chat_id: str) -> Chat:
        async with self.session() as session:
            chat_model = await session.get(ChatModel, chat_id)
            if chat_model:
                return chat_model.to_chat(self)
            return None
        
    async def get_or_create_chat_async(self, database: 'DatabaseInterface', chat_id: str) -> Chat:
        async with self.session() as session:
            chat_model = await session.get(ChatModel, chat_id)
            if chat_model is None:
                chat = Chat(database, chat_id)
                chat_model = ChatModel.from_chat(chat)
                session.add(chat_model)
                await session.commit()
                return chat
            return chat_model.to_chat(database)
    
    async def get_all_chats_async(self) -> List[Chat]:
        async with self.session() as session:
            result = await session.execute(select(ChatModel))
            return [chat_model.to_chat(self) for chat_model in result.scalars()]
    
    async def clear_chat_history_async(self, chat_id: str) -> None:
        async with self.session() as session:
            await session.execute(delete(Chat).where(Chat.chat_id == chat_id))
            await session.commit()
    
    async def clear_all_chats_async(self) -> None:
        async with self.session() as session:
            await session.execute(delete(Chat))
            await session.commit()
    
    async def delete_chat_async(self, chat_id: str) -> None:
        async with self.session() as session:
            await session.delete(await session.get(Chat, chat_id))
            await session.commit()
        

def basic_test():
    client = AIClient(cookie_file="cookies.json",
                       chat_history=True,
                       database=None,
                       logging=True)
    
    print(client.completions.generate("My name is Keva1z.", None, Models.GPT4, 8000))

    input()

    print(client.completions.generate("What is my name?", None, Models.GPT4, 8000))

    input()

    response = client.completions.generate(
        message = "What is on image?",
        agent = None,
        model = Models.GPT4,
        max_tokens = 8000,
        image = "test.jpg"
    )

    print(response)

async def async_test():
    database = AsyncSQLiteDatabase()
    # Даем время на создание таблиц
    await asyncio.sleep(1)  
    
    client = AIClient(cookie_file="cookies.json",
                     chat_history=True,
                     database=database,
                     logging=True)
    
    print(await client.completions.generate_async("My name is Keva1z.", None, Models.GPT4, 8000))

    input()

    print(await client.completions.generate_async("What is my name? Reply only in English", None, Models.GPT4, 8000))

    response = await client.completions.generate_async(
        message = "What is on image?",
        agent = None,
        model = Models.GPT4,
        max_tokens = 8000,
        image = "test.jpg"
    )

    print(response)

if __name__ == "__main__":
    basic_test()
    asyncio.run(async_test())
