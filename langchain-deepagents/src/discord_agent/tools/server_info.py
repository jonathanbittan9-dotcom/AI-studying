from langchain.tools import ToolRuntime , tool
from discord_agent.context.botcontext import BotContext


@tool
async def get_server_info(runtime: ToolRuntime[BotContext]) -> str:
    "lists all the server data"
    guild = runtime.context.guild
    owner = guild.owner.display_name if guild.owner else "unkown"
    server_info = [
        f"server_name: {guild.name}" ,  
        f"owner: {owner}" , 
        f"creation_date: {guild.created_at}" , 
        f"member_count: {guild.member_count}" , 
        f"text_channels{len(guild.text_channels)}" , 
        f"roles: {len(guild.roles)}" , 


    ]
    
    return "\n".join(server_info)

