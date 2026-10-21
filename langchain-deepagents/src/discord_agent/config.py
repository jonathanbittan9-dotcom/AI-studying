import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    model:str

def load_settings() -> Settings:
    return Settings(
        model = os.environ.get("MODEL", "groq:qwen/qwen3-32b")
    )