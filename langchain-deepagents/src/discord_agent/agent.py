from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware
from langgraph.checkpoint.base import BaseCheckpointSaver
from discord_agent.tools import (
    create_roles ,
    remove_roles ,
    list_channels ,
    read_channel ,
    list_roles ,
    get_server_info ,
    create_channels ,
    remove_channels ,

)
from discord_agent.context.botcontext import BotContext
from discord_agent.llm import create_model

SYSTEM_PROMPT = (
    "You are Raider, the AI assistant of a Discord server. "
    "Use your tools to look things up - never guess about the server."
    "Keep answers short and casual, like a Discord message."
)

TOOLS =[
    list_channels ,
    list_roles ,
    get_server_info ,
    read_channel ,
    create_roles ,
    remove_roles ,
    create_channels ,
    remove_channels ,
]

def build_agent(checkpointer: BaseCheckpointSaver):
    return create_deep_agent(
        model=create_model(),
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
        context_schema=BotContext,
        middleware=[TodoListMiddleware()] ,
        checkpointer=checkpointer ,
    )
