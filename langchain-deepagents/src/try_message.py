from discord.discord_agent.llm import create_model

model = create_model()

messages = [
    {"role": "system", "content": "You are Raider, a Discord bot for the server 'Pixel Raiders'. Answer in one short, casual sentence."},
    {"role": "user", "content": "hey, my name is Itay"},
    {"role": "assistant", "content": "Hey Itay, welcome to Pixel Raiders! 👋"},
    {"role": "user", "content": "what's my name?"},
]

replay = model.invoke(messages)

print(replay.content)
print("----")
print(type(replay))
print(replay)
