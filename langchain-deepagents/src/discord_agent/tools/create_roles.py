from langchain.tools import tool , ToolRuntime
from discord_agent.context.botcontext import BotContext
import discord


@tool
async def manage_roles(runtime: ToolRuntime[BotContext]) -> str:
    "creates roles in the discord server"
    guild = runtime.context.guild
    requester = runtime.context.requester
    roles_premissions = []
    premission = requester.guild_permissions.manage_roles
    if premission.guild.roles_premissions.manage_roles:
        premission = "premission to manage roles approved"
    else:
        premission = "premession to manage roles denied"
    roles_premissions.append(f"{requester.name}: {premission}")

    return "\n".join(roles_premissions)


