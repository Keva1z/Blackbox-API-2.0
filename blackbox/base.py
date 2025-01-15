from abc import ABC
from typing import Optional
import logging
from blackbox.cookies import CookieManager
from blackbox import utils
from typing import TYPE_CHECKING
from blackbox.types import DatabaseInterface
from blackbox.database import DictDatabase

if TYPE_CHECKING:
    from blackbox.models import Chat

logger = logging.getLogger(__name__)

class Colors:
    INFO = "\033[94m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    RESET = "\033[0m"
    REQUEST = "\033[95m"
    RESPONSE = "\033[92m"
    DEBUG = "\033[93m"

class BaseAIClient(ABC):
    def __init__(self,
                 base_url: str = "https://www.blackbox.ai",
                 cookie_file: Optional[str] = None,
                 chat_history: bool = True,
                 database: Optional[DatabaseInterface] = None,
                 logging: bool = False):
        self._setup_logging()
        self.logging = logging
        self.base_url = base_url
        self.chat_history = chat_history
        if chat_history:
            if database is None:
                self._log("Database is required when chat_history is True", "WARNING", priority=True)
                self.database = DictDatabase()
            else:
                self.database = database
        else:
            self.database = DictDatabase()

        self._log(f"Initialized as BaseAIClient({self.base_url}, {self.chat_history}, {self.database}, {self.logging})", "DEBUG")

        self._log("Setting up cookies", "DEBUG")
        self.cookie_file = cookie_file
        self.cookie_manager = CookieManager(cookie_file if cookie_file else "cookies.json")
        
        self._log("Setting up headers", "DEBUG")
        self.headers = utils.get_headers()
        self._setup_authentication()

    def _setup_authentication(self) -> None:
        self._log("Setting up authentication", "DEBUG")
        self.headers["cookie"] = self.cookie_manager.cookies

    def _setup_logging(self) -> None:
        """Configure logging for the client."""
        self.logger = logging.getLogger('AIClient')
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _log(self, message: str, log_type: str = "info", priority: bool = False) -> None:
        if not self.logging and not priority:
            return
        
        log_level = getattr(logging, log_type, logging.INFO)
        color = getattr(Colors, log_type, Colors.INFO)
        self.logger.log(log_level, f"{color}{message}{Colors.RESET}")