import requests
import streamlit as st
from io import BytesIO
from PIL import Image

# Load API Key from .streamlit/secrets.toml
API_URL = "https://api-inference.huggingface.co/models/YOUR_MODEL_NAME"
headers = {"Authorization": f"Bearer {st.secrets['huggingface_api_key']}"}
st.write(headers)
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        st.error("Error: " + response.text)
        return None

def generate_image(text_prompt, num_inference_steps, guidance_scale, seed_number):
    with st.spinner("Generating image, please wait..."):
        result = query({
            "inputs": text_prompt,
            "parameters": {
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "seed": seed_number
            }
        })
        if result:
            st.image(result, caption="Generated Image", use_column_width=True)
            st.write("### Parameters Used:")
            st.write(f"- Number of Inference Steps: {num_inference_steps}")
            st.write(f"- Guidance Scale: {guidance_scale}")
            st.write(f"- Seed Number: {seed_number}")
            st.download_button(
                label="Download Image",
                data=BytesIO(result),
                file_name="generated_image.png",
                mime="image/png"
            )

def inpaint_outpaint_image(uploaded_image, mask_prompt, num_inference_steps, guidance_scale, seed_number):
    st.write("### Inpainting/Outpainting")
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    with st.spinner("Applying inpainting/outpainting, please wait..."):
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        
        result = query({
            "inputs": {
                "image": image_bytes,
                "mask_description": mask_prompt
            },
            "parameters": {
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "seed": seed_number
            }
        })
        if result:
            st.image(result, caption="Inpainted/Outpainted Image", use_column_width=True)
            st.download_button(
                label="Download Inpainted/Outpainted Image",
                data=BytesIO(result),
                file_name="inpainted_outpainted_image.png",
                mime="image/png"
            )
