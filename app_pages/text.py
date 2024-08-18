from huggingface_hub import HfApi
from pprint import pprint
import streamlit as st

api = HfApi()
tasks = [
    "sentiment-analysis",
    "text-classification",
    "summarization",
    "question-answering",
    "translation_en_to_fr",
    "text-generation",
]

with st.sidebar:
    task = st.selectbox("Choose Tasks", tasks)
    key_sort = st.radio("Sortby", ["downloads", "likes"])
    limit = st.slider("limit", min_value=5, max_value=100, value=5, step=1)

# Create the instance of the API


# Return the filtered list from the Hub
@st.cache_data
def get_models(tasks="text-classification", sort_by="likes") -> list[dict]:
    models = api.list_models(
        filter=tasks,
        sort=sort_by,
        direction=-1,
        limit=100,
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


models_list = get_models(task, sort_by=key_sort)[:limit]
models_list = sorted(models_list, key=lambda x: x["likes" if key_sort=="downloads" else key_sort], reverse=True)


with st.expander("view models info", icon="ℹ️"):
    st.dataframe(models_list, use_container_width=True)
st.selectbox("choose Model", [model["id"] for model in models_list])
