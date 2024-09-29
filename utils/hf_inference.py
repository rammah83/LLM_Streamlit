import asyncio
import aiohttp
from pprint import pprint
from huggingface_hub import AsyncInferenceClient, InferenceClient


async def get_serverless_models_list(task="text-classification"):
    # Set your Hugging Face API token (get it from your HF account settings)
    with open("././tokens_key.secret", "r", encoding="utf-8") as f:
        api_token = f.read()

    # Set the API endpoint and headers
    endpoint = "https://api-inference.huggingface.co/models"
    headers = {"Authorization": f"Bearer {api_token}"}

    # Call the list_models method with the task filter
    params = {"task": task}

    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint, headers=headers, params=params) as response:
            # Check if the response was successful
            if response.status == 200:
                # Get the list of models
                return await response.json()
            else:
                return f"Error: {response.status}"


async def get_inference(
    inputs, model_id="ProsusAI/finbert", task="text-classification", parameters={}
):
    client = AsyncInferenceClient(
        model=model_id,
        token=open("././tokens_key.secret", "r", encoding="utf-8").read(),
    )
    status = await client.get_model_status()
    if status.state == "Loadable":
        if task == "text-classification":
            return await client.text_classification(inputs)
        elif task == "text-generation":
            return await client.text_generation(inputs)
        elif task == "summarization":
            return await client.summarization(inputs, parameters=parameters)
        elif task == "question-answering":
            return await client.question_answering(**inputs)
        elif task == "translation":
            return await client.translation(inputs, **parameters)
        else:
            return "Task is not loadable"
    else:
        return "Model is not loadable"


def get_inference_from_gradio_client(
    inputs="Write a code in Python that prints hello", model_id="Tonic/Yi-Coder-9B"
):
    from gradio_client import Client

    client = Client(model_id)
    return client.predict(
        system_prompt="You are a helpful coding assistant. Provide clear and concise code examples.",
        user_prompt=inputs,
        max_length=650,
        api_name="/generate_code",
    )


if __name__ == "__main__":
    outputs = asyncio.run(get_inference("I like you"))
    pprint(f"{outputs[0].label} with a score of {outputs[0].score:.2%}")
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
