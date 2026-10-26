from langchain.tools import ToolRuntime , tool
from discord_agent.context.botcontext import BotContext

@tool
async def list_channels(runtime: ToolRuntime[BotContext]) -> str:
    """List all text channels in this Discord server, with their topics."""
    guild = runtime.context.guild

    lines = []
    for channel in guild.text_channels:
        topic = channel.topic or "no topic"
        lines.append(f"#{channel.name} - {topic}")
    
    return "\n".join(lines)

