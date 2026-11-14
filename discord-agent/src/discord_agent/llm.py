from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from discord_agent.config import load_settings

# Ollama's default context window is small, and a deep agent's system prompt plus
# tool descriptions alone take several thousand tokens - without this the start
# of the prompt gets silently cut off.
OLLAMA_CONTEXT_WINDOW = 16384


def create_model() -> BaseChatModel:
    settings = load_settings()
    if settings.model.startswith("ollama:"):
        return init_chat_model(settings.model, num_ctx=OLLAMA_CONTEXT_WINDOW)
    return init_chat_model(settings.model)
