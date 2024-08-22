from narwhals import col
import streamlit as st
from huggingface_hub import HfApi
import tensorflow as tf
from transformers import pipeline

# Variables
api = HfApi()
tasks = [
    "sentiment-analysis",
    "text-classification",
    "summarization",
    "question-answering",
    "translation_en_to_fr",
    "text-generation",
]


# region:Functions
def get_models_list(task="text-classification", sort_key="likes") -> list[dict]:
    """
    Returns a list of dictionaries containing model information.
    """
    models = api.list_models(
        filter=task,
        sort=sort_key,
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


@st.cache_resource
def get_model(task: str, model_id: str):
    """Get a model from the Hub by its task and ID."""
    return pipeline(task=task, model=model_id)


# endregion:Functions

# region:Display Elements commun elements
with st.sidebar:
    task = st.selectbox("Choose Tasks", tasks)


with st.popover("Explore Models", use_container_width=True):
    col1, col2 = st.columns([1, 3])
    key_sort = col1.radio("Sortby", ["downloads", "likes", "last_modified"])
    limit = col1.slider("Limit to", min_value=5, max_value=20, value=5, step=5)
    models_list = get_models_list(task, key_sort)[:limit]
    col2.dataframe(models_list, use_container_width=False)

with st.sidebar:
    selected_model = st.selectbox(
        "Choose Model", [model["id"] for model in models_list]
    )
# endregion:Display Elements commun elements

with st.form(f"{task}"):
    input_text = st.text_area(f"{task.upper()}")
    if task == "summarization":
        text_length=len(input_text.split())
        if text_length < 30:
            st.warning("Text is too short to be summarized")
        else:
            max_length = st.slider(
            "max length",
            min_value=30,
            max_value=int(2 * text_length),
            value=int(1 * text_length),
        )
    if st.form_submit_button("Submit"):
        match task:
            case "sentiment-analysis":
                # prediction
                pipeline_model = get_model(task, selected_model)
                output = pipeline_model(input_text)
                label, score = output[0]["label"].upper(), output[0]["score"]
                # display
                col_label, col_score, col_rest = st.columns(3, gap="small")
                col_label.success(label)
                col_score.metric("Score", value=f"{score:.2%}")
                col_rest.popover("Show all posibilities").write(
                    pipeline_model.model.config.id2label
                )

            case "text-classification":
                # prediction
                pipeline_model = get_model(task, selected_model)
                output = pipeline_model(input_text)
                label, score = output[0]["label"].upper(), output[0]["score"]
                # display
                col_label, col_score, col_rest = st.columns(3, gap="small")
                col_label.success(label)
                col_score.metric("Score", value=f"{score:.2%}")
                col_rest.popover("Show all posibilities").write(
                    pipeline_model.model.config.id2label
                )

            case "summarization":
                # prediction
                pipeline_model = get_model(task, selected_model)
                output = pipeline_model(
                    input_text, max_length=max_length, clean_up_tokenization_spaces=True
                )
                summary_text = output[0]["summary_text"]
                # display
                st.text_area("the summary", value=summary_text)
                st.success(
                    f"Summary Percentage:{len(summary_text.split()) / text_length:.2%}"
                )
                st.write(pipeline_model.model.config.min_length)

            case _:
                st.warning("Not implimented")


# import torch
# st.write(torch.cuda.is_available())
# st.write(tf.test.is_gpu_available(cuda_only=True))
