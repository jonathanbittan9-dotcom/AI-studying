"""Helpers shared by all tools."""

import discord
from langchain.tools import ToolRuntime

from discord_agent.context import BotContext


def get_context(runtime: ToolRuntime[BotContext]) -> tuple[discord.Guild, discord.Member]:
    """Return the server and the member who asked."""
    return runtime.context.guild, runtime.context.requester
