# The main Streamlit application file
from io import BytesIO
import time
import streamlit as st
from utils.image_utils import query_inference_text2img, query_inference_img2img
from PIL import Image
import numpy as np

st.title("Generate, Inpaint, and Outpaint Image with Flux Model")
st.sidebar.header("Parameters")



def generate_image(text_prompt, num_inference_steps, guidance_scale, seed_number):
    start_time = time.time()
    with st.spinner("Generating image, please wait..."):
        # result = query({
        #     "inputs": text_prompt,
        #     "parameters": {
        #         "num_inference_steps": num_inference_steps,
        #         "guidance_scale": guidance_scale,
        #         "seed": seed_number,
        #     }
        # })
        result = query_inference_text2img(text_prompt, num_inference_steps, guidance_scale, seed_number)
        if result:
            st.image(result, caption="Generated Image", use_container_width=False)
            with st.popover("### Parameters Used"):
                st.write(f"- Number of Inference Steps: {num_inference_steps}")
                st.write(f"- Guidance Scale: {guidance_scale}")
                st.write(f"- Seed Number: {seed_number}")
                st.write(f"Time Taken in seconds: {time.time() - start_time:.0f} seconds")

def inpaint_outpaint_image(uploaded_image, mask_prompt, num_inference_steps, guidance_scale, seed_number):
    st.write("### Inpainting/Outpainting")
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    with st.spinner("Applying inpainting/outpainting, please wait..."):
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        
        result = query_inference_img2img(image_bytes, mask_prompt, num_inference_steps, guidance_scale, seed_number)
        if result:
            st.image(result, caption="Inpainted/Outpainted Image", use_container_width =False)
            st.download_button(
                label="Download Inpainted/Outpainted Image",
                data=BytesIO(result),
                file_name="inpainted_outpainted_image.png",
                mime="image/png"
            )

text_prompt = st.text_area("Enter a text prompt to generate an image:")

mode = st.sidebar.selectbox("Select Mode", options=["Generate", "Inpaint", "Outpaint"])
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
