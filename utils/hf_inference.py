import asyncio
from pprint import pprint
from huggingface_hub import AsyncInferenceClient, InferenceClient


async def get_inference(inputs):
    client = AsyncInferenceClient(
        model="ProsusAI/finbert",
        token=open("././tokens_key.secret", "r", encoding="utf-8").read(),
    )
    status = await client.get_model_status()
    if status.state == "Loadable":
        return await client.text_classification(inputs)
    else:
        return "Model is not loadable"


if __name__ == "__main__":
    outputs = asyncio.run(get_inference("I like you"))
    print(f"{outputs[0].label} with a score of {outputs[0].score:.2%}")
    # print(client.health_check())
    models = InferenceClient().list_deployed_models()


# from gradio_client import Client

# client = Client("Tonic/Yi-Coder-9B")
# result = client.predict(
# 		system_prompt="You are a helpful coding assistant. Provide clear and concise code examples.",
# 		user_prompt="Write a quick sort algorithm in Python. write just code no explanation",
# 		max_length=650,
# 		api_name="/generate_code"
# )
# print(result)
