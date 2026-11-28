"""Measure how much a conversation's memory grows, with or without a subagent.

Runs the real agent (real model from .env, real tools) against a FAKE Discord server,
so nothing touches your real server. Two questions in the same thread:
  1. summarize a busy channel  (lots of raw messages to read)
  2. a normal follow-up        (does it still carry those messages?)

Run from the discord-agent folder:
    .venv/bin/python experiments/subagent_demo.py
"""

import asyncio
import os
import time
from types import SimpleNamespace

import discord
from langgraph.checkpoint.memory import InMemorySaver

os.environ.setdefault("DISCORD_TOKEN", "fake")  # settings require these; nothing connects
os.environ.setdefault("DATABASE_URL", "postgresql://fake@localhost/fake")

from discord_agent.agent import build_agent  # noqa: E402
from discord_agent.context import BotContext  # noqa: E402

QUESTIONS = [
    "Summarize what people talked about in #support.",
    "Thanks. Now create a role called Helper.",
]

# 20 realistic, chatty support messages (read_channel reads the latest 20).
SUPPORT_MESSAGES = [
    ("dan", "Hey everyone, my game keeps crashing right after the loading screen. I already reinstalled the drivers and verified the files but it still happens every single time, any ideas?"),
    ("maya", "@dan same thing happened to me last week. It turned out to be the overlay from my recording software, try disabling every overlay you have and launch again."),
    ("dan", "Tried that, no luck. Crash log says something about a shader cache. I'm on a laptop with an integrated GPU and a dedicated one, could it be picking the wrong one?"),
    ("yoni", "Very likely. Go to your graphics settings in Windows, add the game exe and force the high performance GPU. Then delete the shader cache folder and restart."),
    ("dan", "THAT WAS IT. Forcing the dedicated GPU fixed it. Thanks yoni, you're a legend. Two days of crashing and it was one setting."),
    ("noa", "Different issue: I can't join voice channels on the server. It just says 'connecting' forever. Text works fine. Is it my router or something on your side?"),
    ("maya", "@noa usually it's the voice region or a firewall. Try switching the voice region in the channel settings, or allow the app through your firewall."),
    ("noa", "Switched region and it connected instantly. Weird, but it works now. Should someone tell the admins to change the default region?"),
    ("itay", "I'll change the default region later today, thanks for reporting it noa."),
    ("lior", "Question about the tournament next Saturday: do we need to sign up in advance or can we just show up? And is it 1v1 or teams of 3?"),
    ("yoni", "@lior sign up in #tournaments before Friday, it's teams of 3. If you don't have a team, post in #looking-for-group and people will pick you up."),
    ("lior", "Perfect, posting there now. Also is there a rank requirement? I'm still pretty new and don't want to ruin it for others."),
    ("itay", "No rank requirement, it's a fun tournament. New players are very welcome, there's even a beginners bracket this time."),
    ("shira", "Someone keeps sending me DMs with a 'free skins' link claiming to be from this server. Is that legit? It looks super suspicious."),
    ("maya", "@shira NOT legit, never click those. Report the account and block it. We never send links in DMs."),
    ("itay", "Thanks shira, I banned that account. Everyone: we never DM you giveaways. If you get one, report it in here."),
    ("dan", "Small thing: the bot's /ask command is slow sometimes, like 20 seconds before it answers. Is that normal?"),
    ("itay", "@dan yes for now, it runs on a local model on my PC. It'll get faster when we move it to a hosted model."),
    ("noa", "Can we get a channel for sharing clips? #general gets flooded with videos and it's hard to follow the conversation."),
    ("itay", "Good idea noa, I'll create a #clips channel this week."),
]


class FakeChannel:
    def __init__(self, name, topic=None, messages=()):
        self.name = name
        self.topic = topic
        self._messages = list(messages)  # newest first, like Discord

    def history(self, limit):
        async def newest_first():
            for message in self._messages[:limit]:
                yield message

        return newest_first()


def fake_guild():
    messages = [
        SimpleNamespace(author=SimpleNamespace(display_name=author), content=content)
        for author, content in reversed(SUPPORT_MESSAGES)  # Discord gives newest first
    ]
    channels = [FakeChannel("general"), FakeChannel("support", "help and questions", messages)]
    guild = SimpleNamespace(
        name="demo-server",
        owner=SimpleNamespace(display_name="itay"),
        created_at="2026-10-20",
        member_count=7,
        text_channels=channels,
        channels=channels,
        categories=[],
        roles=[SimpleNamespace(name="@everyone", members=[])],
    )

    async def create_role(name, reason=None):
        role = SimpleNamespace(name=name, members=[])
        guild.roles.append(role)
        return role

    guild.create_role = create_role
    return guild


def estimate_tokens(text: str) -> int:
    return len(text) // 4  # rough rule of thumb: ~4 characters per token


def memory_tokens(messages) -> int:
    """Roughly how many tokens of conversation get re-sent on every later model call."""
    total = 0
    for message in messages:
        total += estimate_tokens(str(message.content))
        for call in getattr(message, "tool_calls", None) or []:
            total += estimate_tokens(str(call["args"]))
    return total


async def main():
    guild = fake_guild()
    requester = SimpleNamespace(
        display_name="itay",
        guild_permissions=discord.Permissions(manage_roles=True, manage_channels=True),
    )
    context = BotContext(guild=guild, requester=requester)
    config = {"configurable": {"thread_id": "demo"}}
    agent = build_agent(InMemorySaver())

    seen = 0
    for question in QUESTIONS:
        start = time.monotonic()
        result = await agent.ainvoke({"messages": [question]}, config=config, context=context)
        seconds = time.monotonic() - start
        messages = result["messages"]
        new = messages[seen:]
        seen = len(messages)

        print(f"\n=== {question}")
        for message in new[1:]:  # skip the question itself
            if getattr(message, "tool_calls", None):
                print("  model called:", ", ".join(call["name"] for call in message.tool_calls))
            elif message.type == "tool":
                print(f"  tool {message.name} returned ~{estimate_tokens(str(message.content))} tokens")
        print("  answer:", (messages[-1].text or "")[:200].replace("\n", " "))
        print(f"  took {seconds:.0f}s | messages in memory: {len(messages)} | ~{memory_tokens(messages)} tokens")

    print(
        "\nThose memory tokens are re-sent to the model on every later call in this thread"
        "\n(on top of the system prompt and tool descriptions)."
    )


if __name__ == "__main__":
    asyncio.run(main())
