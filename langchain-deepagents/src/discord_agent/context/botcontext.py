from dataclasses import dataclass
import discord

@dataclass
class BotContext:
    """Information about the current request, provided by our code (never by the LLM)."""
    guild: discord.Guild
    requester: discord.Member