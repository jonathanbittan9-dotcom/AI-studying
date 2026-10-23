from discord_agent.fake_guild import CHANNELS


def read_channel(channel: str) -> str:
    """Read the recent messages in a Discord channel.

    Args:
        channel: The channel name without '#', for example 'general'.
    """
    messages = CHANNELS.get(channel)
    if messages is None:
        return f"Channel '{channel}' does not exist."

    lines = [f"[{m.sent_at:%H:%M}] {m.author}: {m.content}" for m in messages]
    return "\n".join(lines)