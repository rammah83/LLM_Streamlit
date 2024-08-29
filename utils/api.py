from functools import lru_cache
from pprint import pprint
import requests


@lru_cache(maxsize=None)
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


# API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
# headers = {f"Authorization": f"Bearer {open("././tokens_key.secret", "r").read()}"}


def query(payload, model_id="deepset/roberta-base-squad2"):
    API_URL = get_API_URL(model_id)
    headers = get_headers()
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    output = query(
        {
            "inputs": {
                "question": "What is my name?",
                "context": "My name is Clara and I live in Berkeley.",
            },
        }
    )
    pprint(output)
