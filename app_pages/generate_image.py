# The main Streamlit application file
import streamlit as st
from utils.image_utils import query, generate_image, inpaint_outpaint_image
from PIL import Image
import numpy as np

st.title("Generate, Inpaint, and Outpaint Image with Flux Model")
st.sidebar.header("Parameters")

text_prompt = st.text_area("Enter a text prompt to generate an image:")

num_inference_steps = st.sidebar.slider("Number of Inference Steps", min_value=10, max_value=100, value=50, step=5)
guidance_scale = st.sidebar.slider("Guidance Scale", min_value=1.0, max_value=20.0, value=7.5, step=0.5)
seed_number = st.sidebar.number_input("Seed Number", min_value=0, max_value=10000, value=42, step=1)

uploaded_image = st.file_uploader("Upload an image for inpainting or outpainting:", type=["png", "jpg", "jpeg"])
mask_prompt = st.text_area("Enter a description for inpainting or outpainting:")

if st.button("Generate Image"):
    if text_prompt:
        generate_image(text_prompt, num_inference_steps, guidance_scale, seed_number)
    else:
        st.warning("Please enter a text prompt.")

if uploaded_image and mask_prompt:
    if st.button("Apply Inpainting/Outpainting"):
        inpaint_outpaint_image(uploaded_image, mask_prompt, num_inference_steps, guidance_scale, seed_number)

st.sidebar.markdown("Made with Streamlit and Hugging Face API")
