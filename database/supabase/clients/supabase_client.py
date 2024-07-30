from config import SUPABASE_KEY, SUPABASE_URL
from supabase import create_client, Client
from threading import Lock


class SupabaseClient:
    _instance: Client = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    url: str = SUPABASE_URL
                    key: str = SUPABASE_KEY
                    cls._instance = create_client(url, key)

        return cls._instance
