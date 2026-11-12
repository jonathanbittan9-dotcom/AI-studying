import logging
import discord
from discord import app_commands
from discord_agent.config import Settings
from discord_agent.agent import build_agent
from discord_agent.context.botcontext import BotContext
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

log = logging.getLogger(__name__)

DISCORD_MESSAGE_LIMIT = 2000

class RaiderClient(discord.Client):
    def __init__(self , settings:Settings):
        intents = discord.Intents.default()
        intents.message_content = True  #the bot reads what people write
        intents.members = True #see the member list
        super().__init__(intents = intents)

        self.settings = settings
        self.agent = None
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        "Runs one before the bot connects: register the slash commands"
        guild = discord.Object(id=self.settings.guild_id)
        self.pool = AsyncConnectionPool(
            self.settings.database_url,
            kwargs = {"autocommit":True , "row_factory": dict_row} ,  open = False ,
        )
        await self.pool.open()
        self.checkpointer = AsyncPostgresSaver(self.pool)
        await self.checkpointer.setup()
        self.agent = build_agent(self.checkpointer)
        self.tree.add_command(ask, guild=guild)  # register /ask on OUR server
        self.tree.add_command(forget_data , guild=guild)
        await self.tree.sync(guild=guild)
        log.info("Slash commands synced to guild %s", self.settings.guild_id)


    async def close(self) -> None:
        """Runs on shutdown: close the database connection early"""
        await self.pool.close()
        await super().close()



    async def answer(self , question: str , guild: discord.Guild , user: discord.Member , channel_id: int) -> str:
        "ask the agents questions and returns his replay"
        context = BotContext(guild=guild , requester=user)
        config = {"configurable" : {"thread_id": thread_id_for(channel_id , user.id)}}
        result = await self.agent.ainvoke(
            {"messages": [question]},
            context=context,
            config=config,
        )
        for message in result["messages"]:
            log.debug("%s", message.pretty_repr())
        return result["messages"][-1].text[:DISCORD_MESSAGE_LIMIT]

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
            reply = await self.answer(question, message.guild, message.author, message.channel.id)
        await message.reply(reply)

def thread_id_for(channel_id: int  , user_id: int) -> str:
    """decides how the conversation is named"""
    return f"{channel_id}-{user_id}"



@app_commands.command(name="ask" ,  description="Ask Raider anything")
@app_commands.guild_only()
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)
    reply = await interaction.client.answer(
        question, interaction.guild, interaction.user, interaction.channel_id
    )
    await interaction.followup.send(reply)


@app_commands.command(name="forget" , description="tell raider to forget data he collected by you")
@app_commands.guild_only()
async def forget_data(interaction: discord.Interaction):
    thread_id = thread_id_for(interaction.channel_id , interaction.user.id)
    await interaction.client.checkpointer.adelete_thread(thread_id)
    await interaction.response.send_message("Done, I forgot our conversation here.", ephemeral=True)
