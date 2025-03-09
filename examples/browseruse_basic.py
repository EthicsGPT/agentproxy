from allow_agent import *

@request
def request(url, method, headers, body):
    # print the first 100,000 characters of the body
    print("LOG: ", url, str(body)[:100000])
    return True


from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    await agent.run()

asyncio.run(main())