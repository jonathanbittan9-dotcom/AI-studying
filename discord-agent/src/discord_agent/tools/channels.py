"""Tools for reading and managing the server's text channels."""

import discord
from langchain.tools import ToolRuntime, tool

from discord_agent.context import BotContext
from discord_agent.tools._common import get_context

READ_CHANNEL_LIMIT = 20


def normalize_channel_name(name: str) -> str:
    """Turn '#My Channel' into 'my-channel', the way Discord stores text channel names."""
    return name.strip().lstrip("#").lower().replace(" ", "-")


@tool
async def list_channels(runtime: ToolRuntime[BotContext]) -> str:
    """List all text channels in this Discord server, with their topics."""
    guild = runtime.context.guild
    return "\n".join(f"#{channel.name} - {channel.topic or 'no topic'}" for channel in guild.text_channels)


@tool
async def read_channel(channel_name: str, runtime: ToolRuntime[BotContext]) -> str:
    """Read the latest messages in a text channel, oldest first.

    Args:
        channel_name: The channel's name, for example 'general'.
    """
    guild = runtime.context.guild
    channel = discord.utils.get(guild.text_channels, name=normalize_channel_name(channel_name))
    if channel is None:
        available = ", ".join(c.name for c in guild.text_channels)
        return f"Channel '{channel_name}' not found. Available channels: {available}"

    messages = [
        f"{message.author.display_name}: {message.content}"
        async for message in channel.history(limit=READ_CHANNEL_LIMIT)
    ]
    if not messages:
        return f"#{channel.name} has no messages."

    messages.reverse()  # Discord returns newest first
    return "\n".join(messages)


@tool
async def create_channels(name: str, runtime: ToolRuntime[BotContext]) -> str:
    """Create a new text channel in this Discord server.

    Args:
        name: The new channel's name, for example 'memes'.
    """
    guild, requester = get_context(runtime)
    name = normalize_channel_name(name)

    if not requester.guild_permissions.manage_channels:
        return f"{requester.display_name} doesn't have permission to manage channels."
    if discord.utils.get(guild.channels, name=name):
        return f"Channel '{name}' already exists."

    try:
        await guild.create_text_channel(name=name, reason=f"Requested by {requester.display_name} via Raider")
    except discord.Forbidden:
        return "I don't have permission to create channels."
    return f"Created channel #{name}."


@tool
async def remove_channels(name: str, runtime: ToolRuntime[BotContext]) -> str:
    """Delete a channel from this Discord server completely.

    Args:
        name: The exact name of the channel to delete, for example 'memes'.
    """
    guild, requester = get_context(runtime)
    name = normalize_channel_name(name)

    if not requester.guild_permissions.manage_channels:
        return f"{requester.display_name} doesn't have permission to manage channels."
    channel = discord.utils.get(guild.channels, name=name)
    if channel is None:
        return f"Channel '{name}' doesn't exist."

    try:
        await channel.delete(reason=f"Requested by {requester.display_name} via Raider")
    except discord.Forbidden:
        return f"I can't delete '{name}' - I don't have permission."
    return f"Deleted channel #{name}."
