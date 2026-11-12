from langchain.tools import tool , ToolRuntime
from discord_agent.context.botcontext import BotContext
import discord


@tool
async def create_channels(name:str , runtime: ToolRuntime[BotContext]):
    """adds channels to the server"""
    guild = runtime.context.guild
    requester = runtime.context.requester
    if requester.guild_permissions.manage_channels:
        if discord.utils.get(guild.channels , name=name):
            return f"{name} is already exist"
        else:
            try:
                await guild.create_text_channel(name=name , reason = f"requested by {requester.display_name}")
            except discord.Forbidden:
                return "i don't have a premmision to create channels"
    else:
        return f"{requester.display_name} doesn't have the premession to manage channels."

    return f"created the channel {name}"

@tool
async def remove_channels(name:str , runtime: ToolRuntime[BotContext]):
    """removes channels from the server"""
    name = nam.strip().lstrip("#").lower().replace(" " , "-")
    guild = runtime.context.guild
    requester = runtime.context.requester
    if requester.guild_permissions.manage_channels:
        channel = discord.utils.get(guild.channels , name=name)
        if channel:
            try:
                await channel.delete(reason = f"requested by {requester.display_name}")
            except discord.Forbidden:
                return "i don't have a premission to remove channels"
        else:
            return f"{name} is not exist"
    else:
        return f"{requester.display_name} doesn't have premission to manage channels"

    return f"removed channel {channel.name} "

