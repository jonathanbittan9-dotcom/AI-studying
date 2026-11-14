from deepagents import create_deep_agent
from langchain.agents.middleware import SummarizationMiddleware, TodoListMiddleware
from langgraph.checkpoint.base import BaseCheckpointSaver

from discord_agent.context import BotContext
from discord_agent.llm import create_model
from discord_agent.tools import (
    create_channels,
    create_roles,
    get_server_info,
    list_channels,
    list_roles,
    read_channel,
    remove_channels,
    remove_roles,
)

SYSTEM_PROMPT = (
    "You are Raider, the AI assistant of a Discord server. "
    "Use your tools to look things up - never guess about the server. "
    "Keep answers short and casual, like a Discord message. "
    "Before deleting anything, call list_channels or list_roles to verify the exact names."
)
SUMMARIZE_AFTER_TOKENS = 8000
KEEP_RECENT_MESSAGES = 10

TOOLS = [
    list_channels,
    list_roles,
    get_server_info,
    read_channel,
    create_roles,
    remove_roles,
    create_channels,
    remove_channels,
]


def build_agent(checkpointer: BaseCheckpointSaver):
    model = create_model()
    return create_deep_agent(
        model=model,
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
        context_schema=BotContext,
        middleware=[
            TodoListMiddleware(),
            SummarizationMiddleware(
                model=model,
                trigger=("tokens", SUMMARIZE_AFTER_TOKENS),
                keep=("messages", KEEP_RECENT_MESSAGES),
            ),
        ],
        checkpointer=checkpointer,
    )
