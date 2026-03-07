import asyncio
import time
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def fetch_bbc(topic):
    await asyncio.sleep(2)          # Bug 1
    return f"Data from bbc is{topic}"
async def fetch_CNN(topic):
    await asyncio.sleep(2)          # Bug 1
    return f"Data from CNN is{topic}"
async def fetch_fox(topic):
    await asyncio.sleep(2)          # Bug 1
    return f"Data from fox is{topic}"
async def main():
    
    
    while True:
        topic = input("Enter topic: ")
        
        if topic.lower() == "quit":
            break
        start=time.time()
        bbc,cnn,fox=await asyncio.gather(
            fetch_bbc(topic),
            fetch_CNN(topic),
            fetch_fox(topic)
            )


        response=client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role':'system','content':'summarize these news articles concelsely'},
                {"role": "user", "content": f"BBC: {bbc}\nCNN: {cnn}\nfox: {fox}"}
            ]
        )
        print(response.choices[0].message.content)
        print(f'total time:{time.time()-start:.2f}s')
asyncio.run(main())