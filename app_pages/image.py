import json
import requests
import streamlit as st
from PIL import Image
from transformers import pipeline


st.subheader("Hot Dog? Or Not?")
file_name = st.file_uploader("Upload a hot dog candidate image")
st.write(file_name)



headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
def query(filename):
    # with open(filename, "rb") as f:
    #     data = f.read()
    data = Image.open(filename)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))
data = query(file_name)



# pipeline = pipeline(task="image-classification", model="julien-c/hotdog-not-hotdog")
# if file_name is not None:
#     col1, col2 = st.columns(2)

#     image = Image.open(file_name)
#     col1.image(image, use_column_width=True)
#     predictions = pipeline(image)

#     col2.header("Probabilities")
#     for p in predictions:
#         col2.subheader(f"{ p['label'] }: { round(p['score'] * 100, 1)}%")