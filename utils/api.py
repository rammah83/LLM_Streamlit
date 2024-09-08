from functools import lru_cache
from pprint import pprint
import json
import aiohttp
import asyncio
from base64 import b64encode


# API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
# headers = {f"Authorization": f"Bearer {open("././tokens_key.secret", "r").read()}"}


@lru_cache(maxsize=1)
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

headers = get_headers()

async def get_response(API_URL, headers, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, data=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return f"Error: {response.status}, {await response.text()}"

async def query_text(payload, model_id="deepset/roberta-base-squad2", task="text"):
    API_URL = get_API_URL(model_id)
    return await get_response(API_URL, headers, payload)
    
async def query_image(image_file, model_id="google/vit-base-patch16-224"):
    API_URL = get_API_URL(model_id)
    image_data = image_file.getvalue()
    encoded_image = b64encode(image_data).decode("utf-8")
    payload = json.dumps({"inputs": encoded_image})
    return await get_response(API_URL, headers, payload)




async def main():
    inputs = {"inputs": "I like you. I love you"}
    output = await query_text(inputs, model_id="finiteautomata/bertweet-base-sentiment-analysis")

    pprint(output)


if __name__ == "__main__":
    asyncio.run(main())
