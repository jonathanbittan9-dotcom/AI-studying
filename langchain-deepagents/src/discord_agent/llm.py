from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from discord_agent.config import load_settings

def create_model() -> BaseChatModel:
    settings = load_settings()
    return init_chat_model(settings.model)
