from deepagents import create_deep_agent
from dsicord_agent.llm import create_model


class BotContext:
    """Information about the current request, provided by our code (never by the LLM)."""
    guild: discord.Guild
    requester: discord.Member