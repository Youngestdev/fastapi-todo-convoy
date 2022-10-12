from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # database configurations
    WEBHOOK_RECEIVER_URL: Optional[str] = None
    CONVOY_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"