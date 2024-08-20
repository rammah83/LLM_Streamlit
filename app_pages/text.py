import streamlit as st
from huggingface_hub import HfApi
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


# Functions
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


# Display Elements
with st.sidebar:
    task = st.selectbox("Choose Tasks", tasks)

with st.expander("Explore Models", expanded=False):
    col1, col2 = st.columns([1, 3])
    key_sort = col1.radio("Sortby", ["downloads", "likes", "last_modified"])
    limit = col1.slider("Limit to", min_value=5, max_value=20, value=5, step=5)
    models_list = get_models_list(task, key_sort)[:limit]
    col2.dataframe(models_list, use_container_width=False)

with st.sidebar:
    selected_model = st.selectbox(
        "Choose Model", [model["id"] for model in models_list]
    )

with st.form(f"{task}"):
    input_text = st.text_area(f"{task.upper()}")
    if st.form_submit_button("Analyse"):
        model = get_model(task, selected_model)
        output = model(input_text)
        st.success(f"{output[0]['label'].upper()} at {output[0]['score']:.2%}")
        with st.popover("Show all posibilities"):
            st.write(model.model.config.id2label)