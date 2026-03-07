
import asyncio
import time

async def fetch_weather():
    await asyncio.sleep(1)
    return "Weather: Sunny 75°F"

async def fetch_news():
    await asyncio.sleep(1)
    return "News: AI is taking over!"

async def main():
    start = time.time()
    
    weather, news = await asyncio.gather(
        fetch_weather(),
        fetch_news()
    )      # waits 2 more seconds
    
    print(weather)
    print(news)
    print(f"Total time: {time.time() - start:.2f}s")

asyncio.run(main())