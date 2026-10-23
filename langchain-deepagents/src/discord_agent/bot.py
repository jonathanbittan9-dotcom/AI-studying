import logging

import discord
from discord import app_commands

from discord_agent.config import Settings
from discord_agent.llm import create_model

log = logging.getLogger(__name__)

DISCORD_MESSAGE_LIMIT = 2000

SYSTEM_PROMPT = (
    "You are Raider, a friendly Discord bot. "
    "Answer in a short, casual way, like a Discord message."
)


class RaiderClient(discord.Client):
    def __init__(self, settings: Settings):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)

        self.settings = settings
        self.model = create_model()
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        # Commands synced to one guild show up instantly; global sync can take a while.
        if self.settings.guild_id:
            guild = discord.Object(id=self.settings.guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            log.info("Slash commands synced to guild %s", self.settings.guild_id)
        else:
            await self.tree.sync()
            log.info("Slash commands synced globally")

    async def answer(self, question: str) -> str:
        """Turn a user's question into the bot's reply.

        This is the single place the "brain" lives. Today it's one LLM call;
        later it becomes the deep agent.
        """
        reply = await self.model.ainvoke([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ])
        return reply.content[:DISCORD_MESSAGE_LIMIT]


def create_client(settings: Settings) -> RaiderClient:
    client = RaiderClient(settings)

    @client.event
    async def on_ready():
        log.info("Logged in as %s", client.user)

    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return
        if client.user not in message.mentions:
            return

        question = message.content.replace(client.user.mention, "").strip()
        log.info("%s asked in #%s: %s", message.author, message.channel, question)

        async with message.channel.typing():
            reply = await client.answer(question)
        await message.reply(reply)

    @client.tree.command(name="ask", description="Ask Raider anything")
    @app_commands.describe(question="What do you want to ask?")
    async def ask(interaction: discord.Interaction, question: str):
        log.info("%s used /ask: %s", interaction.user, question)
        # Discord drops interactions not answered within 3 seconds; defer buys time.
        await interaction.response.defer(thinking=True)
        reply = await client.answer(question)
        await interaction.followup.send(reply)

    return client
