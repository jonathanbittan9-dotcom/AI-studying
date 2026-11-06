import logging

import discord
from discord import app_commands
from discord_agent.config import Settings
from discord_agent.agent import build_agent
from discord_agent.context.botcontext import BotContext


log = logging.getLogger(__name__)

class RaiderClient(discord.client):
    def __init__(self , settings:Settings):
        intents = discord.Intents.default()
        intents.message_content = True  #the bot reads what people write
        intents.members = members #see the member list
        super.__init__(intents = intents)

        self.settings = settings
        self.agent = build_agent()
        self.tree = app_commands.CommandTree(self)
