import streamlit as st

st.set_page_config(page_title="Ai Tools", layout="wide")
st.title("Tools")

with st.sidebar:
    st.logo(image=r"./res/img/mylogo.jpeg")

pages = {
    "HOME": [st.Page("./app_pages/home.py", title="Home", icon="🏠")],
    "MODELING": [
        st.Page("./app_pages/text.py", title="Text Tasks", icon="🤖"),
        st.Page("./app_pages/image.py", title="Image Tasks", icon="🎨"),
        st.Page("./app_pages/chatwithdoc.py", title="Chatbot Tasks", icon="🧮"),
        st.Page("./app_pages/google_ai.py", title="Google AI Tasks", icon="🤖"),
    ],
    "SYMBOLIC MATHS SOLVER": [
        st.Page("./app_pages/sympy_maths.py", title="Math Tasks", icon="🔢"),
        st.Page("./app_pages/logic_solver.py", title="Logic Tasks", icon="🧠"),
        ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
