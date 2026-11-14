"""Tools for reading and managing the server's roles."""

import discord
from langchain.tools import ToolRuntime, tool

from discord_agent.context import BotContext
from discord_agent.tools._common import get_context


@tool
async def list_roles(runtime: ToolRuntime[BotContext]) -> str:
    """List all the roles in this Discord server and how many members have each one."""
    guild = runtime.context.guild
    return "\n".join(f"{role.name} - {len(role.members)} members" for role in guild.roles)


@tool
async def create_roles(name: str, runtime: ToolRuntime[BotContext]) -> str:
    """Create a new role in this Discord server.

    Args:
        name: The new role's name, for example 'Raider'.
    """
    guild, requester = get_context(runtime)

    if not requester.guild_permissions.manage_roles:
        return f"{requester.display_name} doesn't have permission to manage roles."
    if discord.utils.get(guild.roles, name=name):
        return f"Role '{name}' already exists."

    try:
        await guild.create_role(name=name, reason=f"Requested by {requester.display_name} via Raider")
    except discord.Forbidden:
        return "I don't have permission to create roles."
    return f"Created role {name}."


@tool
async def remove_roles(name: str, runtime: ToolRuntime[BotContext]) -> str:
    """Delete a role from this Discord server completely.

    Args:
        name: The exact name of the role to delete, for example 'Raider'.
    """
    guild, requester = get_context(runtime)

    if not requester.guild_permissions.manage_roles:
        return f"{requester.display_name} doesn't have permission to manage roles."
    role = discord.utils.get(guild.roles, name=name)
    if role is None:
        return f"Role '{name}' doesn't exist."

    try:
        await role.delete(reason=f"Requested by {requester.display_name} via Raider")
    except discord.Forbidden:
        return f"I can't delete '{name}' - it may be above my own role."
    return f"Deleted role {name}."
