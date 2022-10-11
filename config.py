from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # database configurations
    WEBHOOK_RECEIVER_URL: Optional[str] = None

    class Config:
        env_file = ".env"