import json
import os
import re
from datetime import datetime
from typing import Dict, Optional

class CookieManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.cookies = None

        self._load_cookies()

    def _load_cookies(self) -> None:
        if not os.path.exists(self.file_path):
            try:
                cookies_request = input("Enter your cookies: ")
                self.save_cookies(self.parse_cookies(cookies_request))
            except Exception as e:
                raise ValueError(f"Failed to create file: {e}")
        
        with open(self.file_path, 'r') as file:
            try:
                self.cookies = json.load(file)
                self.cookies = '; '.join(f"{key}={value}" for key, value in self.cookies.items())
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON: {e}")

    def parse_cookies(self, cookie_string: str) -> Dict[str, str]:
        try:
            cookie_data = {
                "cookies": dict(
                item.split('=', 1) 
                for item in re.split(r';\s*', cookie_string) 
                if '=' in item
            ),
            "metadata": {
                "created_at": datetime.utcnow().isoformat(),
                "last_modified": datetime.utcnow().isoformat()
            }
            }
            return cookie_data
        except Exception as e:
            raise ValueError(f"Failed to parse cookies: {e}")

    def save_cookies(self, cookie_data: Dict[str, str]) -> None:
        try:
            with open(self.file_path, 'w') as file:
                json.dump(cookie_data, file, indent=4)
        except Exception as e:
            raise ValueError(f"Failed to save cookies: {e}")

    def validate_cookie(self, cookie_string: str) -> bool:
        required_fields = {
            'sessionId',
            '__Host-authjs.csrf-token',
            '__Secure-authjs.session-token'
        }

        try:
            cookie_dict = dict(
                item.split('=', 1) 
                for item in re.split(r';\s*', cookie_string) 
                if '=' in item
            )

            return all(field in cookie_dict['cookies'] for field in required_fields)
        except Exception as e:
            raise ValueError(f"Failed to validate cookies: {e}")