from pyexpat import model
from huggingface_hub import HfApi
from pprint import pprint
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




model_container = st.container()
col1, col2 = model_container.columns([1,3])
with st.sidebar:
    task = st.selectbox("Choose Tasks", tasks)
    if st.checkbox("Explorer Models"):
        key_sort = col1.radio("Sortby", ["downloads", "likes"])
        limit = col1.slider("limit", min_value=5, max_value=20, value=5, step=1)
        # model_container.expander("view models info", icon="ℹ️")
        models_list = get_models(task, sort_by=key_sort)[:limit]
        col2.dataframe(models_list, use_container_width=True)
    else:
        key_sort='downloads'
        limit = 5

    
    models_list = sorted(models_list, key=lambda x: x["likes" if key_sort=="downloads" else key_sort], reverse=True)


with st.sidebar:
    st.selectbox("choose Model", [model["id"] for model in models_list])
