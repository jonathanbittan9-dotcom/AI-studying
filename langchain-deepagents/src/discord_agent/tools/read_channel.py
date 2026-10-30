from langchain.tools import ToolRuntime , tool
from discord_agent.context.botcontext import BotContext

@tool
async def read_channel(runtime: ToolRuntime[botcontext]) -> str:
    channel = discord.utils.get(guild.text_channels , name=channel_name)
    name = message.author.display_name
    latest_messages = []
    async for message in channel.history(limit=20):
        latest_messages.join(f"{name}: {message}")

    return "\n".join(latest_messages)



