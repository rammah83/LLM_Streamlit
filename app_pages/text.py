from huggingface_hub import HfApi
import streamlit as st

# Create the instance of the API
api = HfApi()
tasks = [
    "sentiment-analysis",
    "text-classification",
    "summarization",
    "question-answering",
    "translation_en_to_fr",
    "text-generation",
]

# Return the filtered list from the Hub
@st.cache_data
def get_models(tasks="text-classification", sort_by="likes") -> list[dict]:
    models = api.list_models(
        filter=tasks,
        sort=sort_by,
        direction=-1,
        limit=10,
    )
    # Store as a list od dicts
    return [
        {
            "id": model.modelId,
            "downloads": model.downloads,
            "likes": model.likes,
            "created_at": model.created_at,
        }
        for model in models
    ]



# models_list = get_models(tasks="text-classification", sort_by="downloads")

model_container = st.container()

with st.sidebar:
    task = st.selectbox("Choose Tasks", tasks)
    container_model_selector = st.container()
    with st.popover("Explorer Models"):
        key_sort = st.radio("Sortby", ["downloads", "likes", "created_at"])
        limit = st.slider("Limit to", min_value=5, max_value=20, value=5, step=5)
        # model_container.expander("view models info", icon="ℹ️")
        models_list = get_models(task, sort_by=key_sort)[:limit]

    container_model_selector.selectbox("choose Model", [model["id"] for model in models_list])
st.dataframe(models_list, use_container_width=True)
