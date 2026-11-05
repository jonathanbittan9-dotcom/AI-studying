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
    roles_premissions.append(f"{requester.display_name}: {premission}")

    ## checks if the user has a premission to manage roles
    if  requester.guild_permissions.manage_roles:
        ## checks if the user isn't asking to duplicate an existing role
        if discord.utils.get(guild.roles , name=name):
            return f"role {name} is already exist"
        else:
            ## take action
            add_role = await guild.create_role(name=name , reason=f"{requester.name} wanted to add a new role")
            remove  = await guild.remove_role(name=name , reason=f"requster")
            return f"created role {add_role.name}"

    return "\n".join(roles_premissions)


