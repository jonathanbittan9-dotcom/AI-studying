from langchain.tools import tool , ToolRuntime
from discord_agent.context.botcontext import BotContext


@tool
async def create_channels(runtime: ToolRuntime[BotContext]):
    """adds channels to the server"""
    guild = runtime.context.guild
    requester = runtime.context.requester
    if requester.guild_permissions.manage_channels:
        if discord.utils.get(guild.channels , name=name):
            return f"{name} is already exist"
        else:
            try:
                channel = await create_channel(name=name , reason = f"requested by {requester.display_name}")
            except discord.Forbidden:
                return f"i don't have a premmision to create channels"
    else:
        return f"{requester.display_name} doesn't have the premession to manage roles."

    return f"created the channel {name}"

@tool
async def remove_channels(runtime: ToolRuntime[BotContext]):
    """removes channels from the server"""
    guild = runtime.context.guild
    requester = runtime.context.requester
    if requester.guild_premession.manage_channels:
        if discord.utils.get(guild.channels , name=name):
            try:
                remove_channels = await remove_channel(name=name , reason = f"requested by {requester.display_name}")
            except discord.Forbidden:
                return f"i don't have a premission to remove channels"

    return f"removed channel {name} "

