import asyncio
import time

async def fetch_data(source):
    await asyncio.sleep(2)    #There was no await here
    return f"Data from {source}"

async def main():
    start = time.time()
    
    results = await asyncio.gather(  # Bug 2
        fetch_data("OpenAI"),
        fetch_data("Anthropic"),
        fetch_data("Google")
    )
    
    print(results) #no need of for loop
    
    print(f"Total time: {time.time() - start:.2f}s")

asyncio.run(main())     # no asyncio.run