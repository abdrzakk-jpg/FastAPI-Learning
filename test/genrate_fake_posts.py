
#* A Python Script to Create dummy-posts by user access_token

import httpx
from faker import Faker
import asyncio  
fake = Faker()

BASE_URL = "http://127.0.0.1:8000"
POSTS_ENDPOINT = f"{BASE_URL}/posts/"

NUM_POSTS = 15

access_token = input("Enter access token: ")

headers={
          "Content-Type": "application/json",
          "Authorization": f"Bearer {access_token.strip()}"
}

async def run() -> None:
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        for _ in range(NUM_POSTS):
            post = {
                "title": fake.sentence(nb_words=6),
                "content": fake.text(max_nb_chars=255),
                "published": fake.boolean(),
            }
            
            response = await client.post(POSTS_ENDPOINT, json=post)
            response.raise_for_status()
    print(f"✅ Created {NUM_POSTS} posts")


asyncio.run(run())