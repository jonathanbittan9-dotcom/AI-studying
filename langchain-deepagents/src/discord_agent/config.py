import os
from dataclasses import dataclass
from dotenv import load_dotenv
import logging
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(blue)s%(name)s%(reset)s: %(message)s",
    datefmt="%H:%M:%S",
    log_colors={"DEBUG": "cyan", "INFO": "green", "WARNING": "yellow",
                "ERROR": "red", "CRITICAL": "bold_red"},

    
))

logging.basicConfig(level=logging.DEBUG, handlers=[handler]),

log=logging.getLogger(__name__)



load_dotenv()

@dataclass(frozen=True)
class Settings:
    model:str
    discord_token:str

def load_settings() -> Settings:
    discord_token = os.environ.get("DISCORD_TOKEN")
    if not discord_token:
        log.exception("failed to find the DISCORD_TOKEN")
    return Settings(
        model = os.environ.get("MODEL", "groq:qwen/qwen3-32b") ,
        discord_token = discord_token
    )
    if not discord_token:
        log.exception("failed to find the discord token")