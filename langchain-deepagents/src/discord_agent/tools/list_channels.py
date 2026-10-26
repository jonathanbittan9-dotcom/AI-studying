from langchain.tools import ToolRuntime , tool
from discord_agent.context import botcontext

@tool
async def list_channels(runtime: ToolRuntime[botcontext]) -> str:
    guild = runtime.context.guild

    lines = []
    for channel in guild.text_channels:
        topic = channel.topic or "no topic"
        lines.append(f"#{channel.name} - {topic}")
    
    return"\n .join(lines)"
    
