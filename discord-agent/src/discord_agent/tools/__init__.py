"""The tools the agent can call. Add new tools here and to TOOLS in agent.py."""

from discord_agent.tools.channels import (
    create_channels,
    list_channels,
    read_channel,
    remove_channels,
)
from discord_agent.tools.roles import create_roles, list_roles, remove_roles
from discord_agent.tools.server import get_server_info

__all__ = [
    "create_channels",
    "create_roles",
    "get_server_info",
    "list_channels",
    "list_roles",
    "read_channel",
    "remove_channels",
    "remove_roles",
]
