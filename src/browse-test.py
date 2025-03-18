import os
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
import asyncio

# 无头模式
browser = Browser(
	config=BrowserConfig(
		headless=False,
        disable_security=True
    )
)

os.environ['OPENAI_API_KEY']="sk-proj--xxxxx"

async def main():
    agent = Agent(
        task="搜索AI超元域的GitHub项目并进入",
        llm=ChatOpenAI(model="gpt-4o-mini",),
        browser=browser
    )
    result = await agent.run()
    print(result)

asyncio.run(main())