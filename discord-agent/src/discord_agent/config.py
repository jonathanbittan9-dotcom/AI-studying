import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    model: str
    discord_token: str
    guild_id: int | None  # None -> slash commands are registered globally
    database_url: str


def load_settings() -> Settings:
    discord_token = os.environ.get("DISCORD_TOKEN")
    if not discord_token:
        raise RuntimeError("DISCORD_TOKEN is missing - add it to .env")

    guild_id = os.environ.get("GUILD_ID")

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is missing - add it to .env")

    return Settings(
        model=os.environ.get("MODEL", "groq:openai/gpt-oss-120b"),
        discord_token=discord_token,
        guild_id=int(guild_id) if guild_id else None,
        database_url=database_url,
    )
