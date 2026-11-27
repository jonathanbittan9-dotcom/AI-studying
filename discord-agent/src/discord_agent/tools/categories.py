import discord
from langchain.tools import ToolRuntime, tool

from discord_agent.context import BotContext


@tool
async def create_category(runtime: ToolRuntime[BotContext], name: str):
    """create a new channel category"""
    guild = runtime.context.guild
    requester = runtime.context.requester
    if requester.guild_permissions.manage_channels:
        if discord.utils.get(guild.categories, name=name):
            return "category is already exist."
        else:
            try:
                await guild.create_category(name=name, reason="requested via raider")
                return f"created category {name}"
            except discord.Forbidden:
                return f"failed to create category {name}"
    else:
        return f"the requester {requester.display_name} doesn't have the premmision to manage categories."
