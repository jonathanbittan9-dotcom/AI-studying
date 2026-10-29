from deepagents import create_deep_agent

from discord_agent.context.botcontext import BotContext
from discord_agent.llm import create_model
from discord_agent.tools.list_channels import list_channels
from discord_agent.tools.roles import list_roles
from discord_agent.tools.server_info import get_server_info

SYSTEM_PROMPT = (
    "You are Raider, the AI assistant of a Discord server. "
    "Use your tools to look things up - never guess about the server. "
    "Keep answers short and casual, like a Discord message."
)


def build_agent():
    return create_deep_agent(
        model=create_model(),
        tools=[list_channels, list_roles , get_server_info],
        system_prompt=SYSTEM_PROMPT,
        context_schema=BotContext,
    )