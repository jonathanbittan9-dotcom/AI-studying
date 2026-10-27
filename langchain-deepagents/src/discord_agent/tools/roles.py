from langchain import ToolRuntime , tool
from discord_agent.context.botcontext import BotContext


@tool
async def list_roles(runtime: ToolRuntime[BotContext]) -> str:
    "list all the roles of the server"
    guild = runtime.context.guild
    roles_server = []

    for roles in guild.roles:
        roles_server.append(f"{roles} - {len(roles.members)}")
    
    return "\n".join(roles_server)
