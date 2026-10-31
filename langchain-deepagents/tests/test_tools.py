"""Smoke tests for the agent's tools, using fake Discord objects (no network, no LLM)."""

import asyncio
from datetime import datetime
from types import SimpleNamespace

from discord_agent.tools.list_channels import list_channels
from discord_agent.tools.read_channel import read_channel
from discord_agent.tools.roles import list_roles
from discord_agent.tools.server_info import get_server_info


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


def fake_message(author, content, hour, minute):
    return SimpleNamespace(
        author=SimpleNamespace(display_name=author),
        content=content,
        created_at=datetime(2026, 10, 20, hour, minute),
    )


def fake_guild():
    general = FakeChannel("general", messages=[
        fake_message("emily", "not yet lol", 14, 7),
        fake_message("jake", "anyone beat the boss?", 14, 5),
    ])
    return SimpleNamespace(
        name="bot-testing",
        owner=SimpleNamespace(display_name="itay"),
        created_at=datetime(2026, 10, 20),
        member_count=3,
        text_channels=[general, FakeChannel("announcements", topic="news")],
        roles=[
            SimpleNamespace(name="@everyone", members=[1, 2, 3]),
            SimpleNamespace(name="Manager", members=[1]),
        ],
    )


def run_tool(tool, guild, **args):
    """Call a tool's function directly, with a fake runtime carrying our fake guild."""
    runtime = SimpleNamespace(context=SimpleNamespace(guild=guild, requester=None))
    return asyncio.run(tool.coroutine(runtime=runtime, **args))


def test_list_channels():
    result = run_tool(list_channels, fake_guild())
    assert "#general" in result
    assert "#announcements - news" in result


def test_list_roles():
    result = run_tool(list_roles, fake_guild())
    assert "Manager - 1" in result


def test_get_server_info_without_owner():
    guild = fake_guild()
    guild.owner = None  # Discord sometimes hasn't sent the owner yet
    result = run_tool(get_server_info, guild)
    assert "bot-testing" in result


def test_read_channel_oldest_first():
    result = run_tool(read_channel, fake_guild(), channel_name="general")
    assert result.index("jake") < result.index("emily")


def test_read_channel_unknown_channel_lists_real_ones():
    result = run_tool(read_channel, fake_guild(), channel_name="memes")
    assert "general" in result and "announcements" in result


def test_tools_hide_runtime_from_the_llm():
    # The LLM must never see or fill in `runtime` - only real arguments.
    assert list_roles.args == {}
    assert list(read_channel.args) == ["channel_name"]
