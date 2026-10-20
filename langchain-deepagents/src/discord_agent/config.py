import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class settings:
    model:str

def load_settings() -> settings:
    return settings(
        model = os.environ.get("MODEL", "groq:qwen/qwen3-32b")
    )