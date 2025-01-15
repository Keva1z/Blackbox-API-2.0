from sqlalchemy import Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from blackbox.models import Chat, Message

Base = declarative_base()

class ChatModel(Base):
    __tablename__ = 'chats'
    
    chat_id = Column(String, primary_key=True)
    created_at = Column(String)
    chat_metadata = Column(JSON)
    messages = Column(JSON)  # Будем хранить сообщения как JSON

    def to_chat(self, database) -> 'Chat':
        from blackbox.models import Chat, Message
        
        chat = Chat(database, self.chat_id)
        chat.created_at = self.created_at
        chat.metadata = self.chat_metadata
        
        # Конвертируем JSON сообщений обратно в объекты Message
        for msg_dict in self.messages:
            message = Message(
                content=msg_dict['content'],
                role=msg_dict['role'],
                id=msg_dict['id'],
                timestamp=msg_dict.get('timestamp'),
                image=msg_dict.get('image')
            )
            chat.messages.append(message)
            
        return chat

    @staticmethod
    def from_chat(chat: 'Chat') -> 'ChatModel':
        return ChatModel(
            chat_id=chat.chat_id,
            created_at=chat.created_at,
            chat_metadata=chat.metadata,
            messages=[{
                'content': msg.content,
                'role': msg.role,
                'id': msg.id,
                'timestamp': msg.timestamp,
                'image': msg.image
            } for msg in chat.messages]
        )
