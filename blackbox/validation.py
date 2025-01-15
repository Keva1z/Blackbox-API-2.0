import os
import json
from datetime import datetime, timedelta
import re
import aiohttp
import requests

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from blackbox.client import AIClient

class Validation:
    def __init__(self, client: "AIClient"):
        self.client = client
        self._validated_cache_file = "validated_cache.json"
        self._validated_cache_ttl = timedelta(hours=4)
        self._last_validated_value = None

        self._load_validated_from_cache()


    def _load_validated_from_cache(self) -> None:
        """Load validated value from cache file if it exists and is not expired."""
        try:
            if os.path.exists(self._validated_cache_file):
                with open(self._validated_cache_file, 'r') as f:
                    cache_data = json.load(f)
                    cached_time = datetime.fromisoformat(cache_data['timestamp'])
                    if datetime.utcnow() - cached_time < self._validated_cache_ttl:
                        self._last_validated_value = cache_data['value']
                        self.client._log(f"Loaded validated value from cache: {self._last_validated_value}", "DEBUG")
        except Exception as e:
            self.client._log(f"Failed to load validated cache: {str(e)}", "ERROR")

    def _save_validated_to_cache(self, value: str) -> None:
        """Save validated value to cache file."""
        try:
            cache_data = {
                'value': value,
                'timestamp': datetime.utcnow().isoformat()
            }
            with open(self._validated_cache_file, 'w') as f:
                json.dump(cache_data, f)
            self.client._log("Saved validated value to cache", "DEBUG")
        except Exception as e:
            self.client._log(f"Failed to save validated cache: {str(e)}", "ERROR")

    async def fetch_validated_async(self) -> str:
        """Fetch validated value from Blackbox website JS files.
        
        Returns:
            str: Validated value for API requests
        """
        # Проверяем кэш в памяти
        if self._last_validated_value:
            return self._last_validated_value

        # Пытаемся получить новое значение

        self.client._log("Fetching validated value from Blackbox website", "DEBUG")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.client.base_url) as response:
                    if response.status != 200:
                        self.client._log("Failed to load the main page", "ERROR")
                        return self._last_validated_value
                    
                    page_content = await response.text()
                    js_files = re.findall(r'static/chunks/\d{4}-[a-fA-F0-9]+\.js', page_content)

                key_pattern = re.compile(r'w="([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"')

                for js_file in js_files:
                    js_url = f"{self.client.base_url}/_next/{js_file}"
                    async with session.get(js_url) as js_response:
                        if js_response.status == 200:
                            js_content = await js_response.text()
                            match = key_pattern.search(js_content)
                            if match:
                                validated_value = match.group(1)
                                self._last_validated_value = validated_value
                                # Сохраняем новое значение в кэш
                                self._save_validated_to_cache(validated_value)
                                return validated_value
                                
            except Exception as e:
                self.client._log(f"Error fetching validated value: {str(e)}", "ERROR")

        return self._last_validated_value
    
    def fetch_validated(self) -> str:
        if self._last_validated_value:
            return self._last_validated_value
        
        try:
            response = requests.get(self.client.base_url)
            if response.status_code != 200:
                self.client._log("Failed to load the main page", "ERROR")
                return self._last_validated_value
            
            page_content = response.text
            js_files = re.findall(r'static/chunks/\d{4}-[a-fA-F0-9]+\.js', page_content)

            key_pattern = re.compile(r'w="([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"')

            for js_file in js_files:
                js_url = f"{self.client.base_url}/_next/{js_file}"
                js_response = requests.get(js_url)
                if js_response.status_code == 200:
                    js_content = js_response.text
                    match = key_pattern.search(js_content)
                    if match:
                        validated_value = match.group(1)
                        self._last_validated_value = validated_value
                        self._save_validated_to_cache(validated_value)
                        return validated_value

            return self._last_validated_value
        except Exception as e:
            self.client._log(f"Error fetching validated value: {str(e)}", "ERROR")

        return self._last_validated_value
