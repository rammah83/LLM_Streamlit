import os
import time
from tracemalloc import start
from huggingface_hub import InferenceClient
import requests
import streamlit as st
from io import BytesIO
from PIL import Image

# Load API Key from .streamlit/secrets.toml
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": f"Bearer {st.secrets['huggingface_api_key']}"}

def query_requests(payload):
    """
    Sends a POST request to the specified API URL with the given payload.

    Args:
        payload (dict): The JSON payload to be sent in the POST request.

    Returns:
        bytes: The content of the response if the request is successful.
        None: If the request fails, logs an error message and returns None.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        st.error("Error: " + response.text)
        return None

def query_inference_text2img(
    text_prompt: str,
    num_inference_steps: int,
    guidance_scale: float,
    seed_number: int,
    size: tuple[int, int] = (512, 512)
) -> Image.Image:
    """
    Generates an image from a text prompt using the specified inference client.

    Args:
        text_prompt (str): The text input for which an image will be generated.
        num_inference_steps (int): The number of inference steps to be used in generating the image.
        guidance_scale (float): The guidance scale to influence the image generation process.
        seed_number (int): The seed number for randomization in image generation.
        size (tuple[int, int], optional): The size of the generated image. Defaults to (512, 512).

    Returns:
        Image.Image: The generated image based on the provided text prompt and parameters.
    """
    client = InferenceClient(
        model="black-forest-labs/FLUX.1-dev",
        token=st.secrets["huggingface_api_key"],
    )
    image_bytes = client.text_to_image(
        prompt=text_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        seed=seed_number,
        width=size[0],
        height=size[1],
    )
    return image_bytes

def query_inference_img2img(
    uploaded_image: Image.Image,
    text_prompt: str,
    num_inference_steps: int,
    guidance_scale: float,
    seed_number: int,
    size: tuple[int, int] = (512, 512)
) -> Image.Image:
    client = InferenceClient(
        model="black-forest-labs/FLUX.1-dev",
        token=st.secrets["huggingface_api_key"],
    )
    image_bytes = client.image_to_image(
        image=uploaded_image,
        prompt=text_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        seed=seed_number,
        width=size[0],
        height=size[1],
    )
    return image_bytes