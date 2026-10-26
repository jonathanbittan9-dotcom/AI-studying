from deepagents import create_deep_agent

from discord_agent.context.botcontext import BotContext
from dsicord_agent.llm import create_model
from discord_agent.tools.list_channels import list_channels

SYSTEM_PROMPT = {
    "You are Raider, the AI assistant of a Discord server. "
    "Use your tools to look things up - never guess about the server. "
    "Keep answers short and casual, like a Discord message."
}


def build_agent():
    return create_deep_agent(
        model=create_model ,
        tools=[list_channels] ,
        system_prompt=SYSTEM_PROMPT ,
        context_schema = BotContext ,
    )