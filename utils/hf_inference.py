import asyncio
from pprint import pprint
from huggingface_hub import AsyncInferenceClient, InferenceClient


async def get_inference(inputs, model_id="ProsusAI/finbert", task="text-classification", parameters={}):
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
            return await client.translation(inputs)
        else:
            return "Task is not loadable"
    else:
        return "Model is not loadable"


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
