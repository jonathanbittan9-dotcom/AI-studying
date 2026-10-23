from dataclasses import dataclass
from datetime import datetime , timedelta

@dataclass
class Message:
    author: str
    content: str
    sent_at: datetime


def minutes_ago(minutes:int) -> datatime:
    return datetime.now() - timedelta(minutes=minutes)

CHANNELS: dict[str, list[Message]] = {
    "announcements": [
        Message("mike", "Patch 2.3 is live! New boss 'Frost Wyrm', crafting rework, and double XP this weekend.", minutes_ago(180)),
    ],
    "general": [
        Message("jake", "anyone beat the frost wyrm yet?", minutes_ago(30)),
        Message("emily", "not yet, its ice breath one-shots me lol", minutes_ago(28)),
        Message("jake", "fire resist potions help a lot", minutes_ago(25)),
        Message("spammer123", "FREE NITRO >>> sketchy.link/free", minutes_ago(20)),
        Message("emily", "is the crafting rework good tho?", minutes_ago(10)),
    ],
}