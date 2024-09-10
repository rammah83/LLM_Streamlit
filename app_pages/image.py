import asyncio
import streamlit as st
from utils import api

# Variables
tasks = [
    "image-classification",
    "object-detection",
    "image-to-text",
    "image-segmentation",
]

# region:Display Elements commun elements
with st.sidebar:
    task = st.selectbox("Choose Tasks", tasks, on_change=api.get_API_URL.cache_clear())

st.title("Image Classification with Hugging Face API")
selected_model = "google/vit-base-patch16-224"
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
col_img, col_info = st.columns([1, 1], gap="large")
if uploaded_file is not None:
    col_img.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    result = asyncio.run(api.query_image(uploaded_file, model_id=selected_model))
    if isinstance(result, list):
        with col_info:
            st.write("Classification Results:")
            for item in result:
                col_label, col_score = st.columns([2, 1], gap="small")
                col_label.progress(item["score"], text=item["label"])
                col_score.write(f"{item['score']:.2%}")
                # st.write(f"Label: {item['label']}, Score: {item['score']:.4f}")
    else:
        st.error(result)


if __name__ == "__main__":
    asyncio.run(api.query_image(uploaded_file))
