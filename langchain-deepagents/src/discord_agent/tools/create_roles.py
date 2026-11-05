from langchain.tools import tool , ToolRuntime
from discord_agent.context.botcontext import BotContext
import discord


@tool
async def manage_roles(name: str, runtime: ToolRuntime[BotContext]) -> str:
    "creates roles in the discord server"
    guild = runtime.context.guild
    requester = runtime.context.requester
    roles_premissions = []
    premission = requester.guild_permissions.manage_roles
    if premission:
        premission = "premission to manage roles approved"
    else:
        premission = "premession to manage roles denied"
    roles_premissions.append(f"{requester.name}: {premission}")

    if  requester.guild_permissions.manage_roles:
        role = await guild.create_role(name=name)
        return f"created role {role.name}"

    return "\n".join(roles_premissions)


