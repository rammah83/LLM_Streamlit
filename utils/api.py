from functools import lru_cache
from pprint import pprint
import aiohttp
import asyncio


# API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
# headers = {f"Authorization": f"Bearer {open("././tokens_key.secret", "r").read()}"}


@lru_cache(maxsize=2)
def get_API_URL(model_id):
    try:
        return f"https://api-inference.huggingface.co/models/{model_id}"
    except KeyError:
        print("model id not found")


@lru_cache(maxsize=None)
def get_headers():
    try:
        with open("././tokens_key.secret", "r") as f:
            return {"Authorization": f"Bearer {f.read()}"}
    except FileNotFoundError:
        print("key file not found")
    except KeyError:
        print("key not found")


async def query(payload, model_id="deepset/roberta-base-squad2", task="text"):
    API_URL = get_API_URL(model_id)
    headers = get_headers()
    async with aiohttp.ClientSession() as session:
        try:
            if task == "text":
                async with session.post(API_URL, headers=headers, json=payload) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise Exception(await response.text())
        except Exception as e:
            print(e)
            return None


async def main():
    inputs = {"inputs": "I like you. I love you"}
    output = await query(inputs, model_id="finiteautomata/bertweet-base-sentiment-analysis")

    pprint(output)


if __name__ == "__main__":
    asyncio.run(main())
