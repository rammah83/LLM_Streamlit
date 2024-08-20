import streamlit as st

st.set_page_config(page_title='Ai Tools', layout='wide')
st.title("Ai Tools")

pages = {
    "HOME": [st.Page("./app_pages/home.py", title="Home", icon="🏠")],
    "MODELING": [
        st.Page("./app_pages/text.py", title="Text Tasks", icon="🤖"),
        st.Page("./app_pages/image.py", title="Image Tasks", icon="🧮"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()