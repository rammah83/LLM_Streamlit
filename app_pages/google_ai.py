import google.generativeai as genai
import streamlit as st

genai.configure(api_key="AIzaSyB279brH54LJ97kqJE5N0RSxsX-_YSY6uQ")

def get_google_ai_response(prompt="Write a story about a magic backpack.", model_id="gemini-1.5-flash"):
    model = genai.GenerativeModel(model_id)
    response = model.generate_content(prompt)
    return response.text


with st.form("my_form"):
    prompt = st.text_input("Enter your prompt")
    if st.form_submit_button("Submit"):
        with st.spinner("Generating..."):
            response = get_google_ai_response(prompt)
            st.write(response)
    
if __name__ == "__main__":
    get_google_ai_response()