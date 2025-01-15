from blackbox.base import BaseAIClient
from blackbox.completions import Completions
from blackbox.validation import Validation

from typing import Optional
from blackbox.base import DatabaseInterface

class AIClient(BaseAIClient):
    def __init__(self, cookie_file: Optional[str] = None,
                chat_history: bool = True,
                 database: Optional[DatabaseInterface] = None,
                 logging: bool = False):
        
        super().__init__(cookie_file=cookie_file, chat_history=chat_history, database=database, logging=logging)
        self.completions = Completions(self)
        self.validation = Validation(self)


