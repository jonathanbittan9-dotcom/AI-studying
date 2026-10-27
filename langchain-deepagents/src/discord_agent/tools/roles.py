from langchain.tools import ToolRuntime, tool

from discord_agent.context.botcontext import BotContext


@tool
async def list_roles(runtime: ToolRuntime[BotContext]) -> str:
    """List all the roles in this Discord server and how many members have each one."""
    guild = runtime.context.guild
    roles_server = []

    for role in guild.roles:
        roles_server.append(f"{role.name} - {len(role.members)} members")

    return "\n".join(roles_server)
