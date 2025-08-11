from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

settings = Settings()