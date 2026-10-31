from langchain.tools import ToolRuntime , tool
from discord_agent.context.botcontext import BotContext
import discord

@tool
async def read_channel(channel_name:str , runtime: ToolRuntime[BotContext]) -> str:
    """shows the messages of the channels"""
    guild = runtime.context.guild
    channel = discord.utils.get(guild.text_channels , name=channel_name)
    if channel is None:
        availbale = ",".join(c.name for c in guild.text_channels)
        return f"{channel_name} is not found. availbale channels: {availbale}"

    latest_messages = []

    async for message in channel.history(limit=20):
        name = message.author.display_name
        latest_messages.append(f"{name}: {message.content}")

    if not latest_messages:
        return f"{channel.name} has no messages"

    latest_messages.reverse()
    return "\n".join(latest_messages)


