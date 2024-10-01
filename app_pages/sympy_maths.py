import sympy as sp
from string import ascii_letters
import streamlit as st  # type: ignore

st.logo("https://t3.ftcdn.net/jpg/05/51/43/56/360_F_551435602_v0rxhHEIgbQNWozIjcgJOR2Nmp1SINMV.jpg")
st.title("Maths :blue[cool] :sunglasses:")
st.subheader("This is our first app with Streamlit!")

variables = st.multiselect("Select the math symbols", list(ascii_letters))
functionality = st.selectbox("Select funtionality", ["solve", "simplify", "derive", "integrate"])

expression = st.text_input("Enter your equation here")
if st.button("Submit"):
    match functionality:
        case "solve":
            sols = sp.solve(expression, variables)
            for sol in sols:
                st.write(f"solution is : {sol}")
        case "simplify":
            st.write(sp.simplify(expression))
        case "derive":
            st.write(sp.diff(expression))
        case "integrate":
            st.write(sp.integrate(expression))
        case _:
            st.write("Wrong input")

