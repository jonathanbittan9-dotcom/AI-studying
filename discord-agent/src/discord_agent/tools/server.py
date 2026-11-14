"""Tools for general information about the server."""

from langchain.tools import ToolRuntime, tool

from discord_agent.context import BotContext


@tool
async def get_server_info(runtime: ToolRuntime[BotContext]) -> str:
    """Get general information about this Discord server: name, owner, creation date and sizes."""
    guild = runtime.context.guild
    owner = guild.owner.display_name if guild.owner else "unknown"
    return "\n".join(
        [
            f"server_name: {guild.name}",
            f"owner: {owner}",
            f"creation_date: {guild.created_at}",
            f"member_count: {guild.member_count}",
            f"text_channels: {len(guild.text_channels)}",
            f"roles: {len(guild.roles)}",
        ]
    )
