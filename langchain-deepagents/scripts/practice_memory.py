import asyncio

from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver
from discord_agent.llm import create_model


agent = create_deep_agent(model = create_model() , checkpointer=InMemorySaver())

async def ask(question:str , thread_id:str) -> None:
    config = {"configurable": {"thread_id": question}}
    result = await agent.ainvoke({"messages": [question]} , config=config)
    print(result['messages'][-1].text)

async def main():
    await ask("my name is linux , remember it")
    await ask("what is my name?")

if __name__ == "__main__":
    ayncio.run(main())
