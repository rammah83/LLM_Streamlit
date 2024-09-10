from functools import lru_cache
from huggingface_hub import HfApi
from transformers import pipeline
# import asyncio


hf_api = HfApi()
# region:Functions
def get_models_list(
    task="text-classification", sort_key="trending", language: str | list[str] = "en"
) -> list[dict]:
    """
    Returns a list of dictionaries containing model information.
    """
    models = hf_api.list_models(
        filter=task,
        search="en_to_fr" if task == "translations" else None,
        sort=sort_key,
        language=language,
        direction=-1,
        limit=10,
    )

    # Store as a list of dictionaries
    return [
        {
            "id": model.modelId,
            "downloads": model.downloads,
            "likes": model.likes,
            "created_at": model.created_at.date(),
        }
        for model in models
    ]


@lru_cache(maxsize=None)
def get_pipeline_model(task: str, model_id: str):
    """Get a model from the Hub by its task and ID."""
    return pipeline(task=task, model=model_id)

