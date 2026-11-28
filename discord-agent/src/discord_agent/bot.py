import logging

import discord
from discord import app_commands
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.types import Command
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from discord_agent.agent import build_agent
from discord_agent.config import Settings
from discord_agent.context import BotContext

log = logging.getLogger(__name__)

DISCORD_MESSAGE_LIMIT = 2000


class RaiderClient(discord.Client):
    def __init__(self, settings: Settings):
        intents = discord.Intents.default()
        intents.message_content = True  # the bot reads what people write
        intents.members = True  # see the member list
        super().__init__(intents=intents)

        self.settings = settings
        self.agent = None
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        """Runs once before the bot connects: open the database and register the slash commands."""
        self.pool = AsyncConnectionPool(
            self.settings.database_url,
            kwargs={"autocommit": True, "row_factory": dict_row},
            open=False,
        )
        await self.pool.open()
        self.checkpointer = AsyncPostgresSaver(self.pool)
        await self.checkpointer.setup()
        self.agent = build_agent(self.checkpointer)
        commands = [ask, forget_data, list_history, shared_thread]

        if self.settings.guild_id:
            # test server: commands update instantly
            guild = discord.Object(id=self.settings.guild_id)
            for command in commands:
                self.tree.add_command(command, guild=guild)
            await self.tree.sync(guild=guild)
            log.info("Slash commands synced to guild %s", self.settings.guild_id)
        else:
            # every server the bot is in
            for command in commands:
                self.tree.add_command(command)
            await self.tree.sync()
            log.info("Slash commands synced globally")

    async def close(self) -> None:
        """Runs on shutdown: close the database connections."""
        await self.pool.close()
        await super().close()

    async def answer(self, question: str, guild: discord.Guild, user: discord.Member, channel_id: int , shared: Bool = False):
        """Ask the agent a question. Returns (reply, view); view is None unless approval is needed."""
        context = BotContext(guild=guild, requester=user)
        if shared:
            config = {"configurable": {"thread_id": (f"{channel_id } - shared")}}
        else:
            config = {"configurable": {"thread_id": thread_id_for(channel_id , user.id)}}


        result = await self.agent.ainvoke(
            {"messages": [question]},
            context=context,
            config=config,
        )
        for message in result["messages"]:
            log.debug("%s", message.pretty_repr())
        if result.get("__interrupt__"):
            log.debug(result.get("__interrupt__"))
            view = Approval_view(self, config, context, user.id)
            return "i want to delete part of the data of this server, OK?", view
        return result["messages"][-1].text[:DISCORD_MESSAGE_LIMIT], None

    async def on_ready(self):
        log.info("Logged in as %s", self.user)

    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return
        if self.user not in message.mentions:
            return

        question = message.content.replace(self.user.mention, "").strip()
        log.info("%s asked in #%s: %s", message.author, message.channel, question)

        async with message.channel.typing():
            reply, view = await self.answer(question, message.guild, message.author, message.channel.id)
        if view:
            await message.reply(reply, view=view)
        else:
            await message.reply(reply)


class Approval_view(discord.ui.View):
    def __init__(self, bot, config, context, requester_id):
        super().__init__(timeout=300)
        self.bot = bot
        self.config = config
        self.context = context
        self.requester_id = requester_id

    async def resume(self, interaction, decision_type):
        if interaction.user.id != self.requester_id:
            await interaction.response.send_message("Not your request", ephemeral=True)
            return
        else:
            await interaction.response.defer()
            result = await self.bot.agent.ainvoke(
                Command(resume={"decisions": [{"type": decision_type}]}),
                context=self.context,
                config=self.config,
            )
            await interaction.followup.send(result["messages"][-1].text or "Done")
            self.stop()

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.danger)
    async def approve(self, interaction, button):
        await self.resume(interaction, "approve")

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.secondary)
    async def reject(self, interaction, button):
        await self.resume(interaction, "reject")


def thread_id_for(channel_id: int, user_id: int) -> str:
    """One conversation per user per channel."""
    return f"{channel_id}-{user_id}"


@app_commands.command(name="ask", description="Ask Raider anything")
@app_commands.guild_only()
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)
    reply, view = await interaction.client.answer(
        question, interaction.guild, interaction.user, interaction.channel_id
    )
    if view:
        await interaction.followup.send(reply, view=view)
    else:
        await interaction.followup.send(reply)


@app_commands.command(name="forget", description="Make Raider forget your conversation in this channel")
@app_commands.guild_only()
async def forget_data(interaction: discord.Interaction):
    thread_id = thread_id_for(interaction.channel_id, interaction.user.id)
    await interaction.client.checkpointer.adelete_thread(thread_id)
    await interaction.response.send_message("Done, I forgot our conversation here.", ephemeral=True)


@app_commands.command(name="history", description="summarizes you're chat history with raider")
@app_commands.guild_only()
async def list_history(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)

    try:
        history = []
        async for message in interaction.channel.history(limit=100):
            if message.author.id in (interaction.user.id, interaction.client.user.id):
                content = message.content or "[message has no text]"
                history.append(f"{message.author.display_name}: {content}")
    except discord.Forbidden:
        await interaction.followup.send(
            "I need the Read Message History permission to show this channel's history.",
            ephemeral=True,
        )
        return

    if not history:
        await interaction.followup.send(
            "I couldn't find any messages from you or Raider in the latest 100 channel messages.",
            ephemeral=True,
        )
        return

    # Discord returns newest messages first; show them in conversation order.
    history.reverse()
    response = "\n".join(history)
    for start in range(0, len(response), DISCORD_MESSAGE_LIMIT):
        await interaction.followup.send(response[start : start + DISCORD_MESSAGE_LIMIT], ephemeral=True)

@app_commands.command(name="shared_conversation", description="open a shared conversation with everyone in the current channel you are in")
@app_commands.guild_only()
async def shared_thread(interaction: discord.Interaction , question:str):
    await interaction.response.defer(thinking=True)
    replay, view = await interaction.client.answer(
        question, interaction.guild, interaction.user , interaction.channel_id , shared=True
    )
    if view:
        await interaction.followup.send(replay, view=view)
    else:
        await interaction.followup.send(replay)
