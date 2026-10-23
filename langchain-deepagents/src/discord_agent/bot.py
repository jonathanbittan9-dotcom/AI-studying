import discord
from discord_agent.config import load_settings , log
from discord_agent.llm import create_model

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    log.info("bot is online")

@client.event
async def on_message(message:discord.Message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        await message.channel.send(f"Hi {message.author.display_name}! I'm alive 👋")
        log.info("answered the user")
   
@client.tree.command(name="llm" , description="talk to a llm")
async def llm_call(interaction: discord.Interaction):
    await interaction.response.send_message({create_model})



def main():
    settings = load_settings()
    client.run(settings.discord_token)


if __name__ == "__main__":
    main()