from turtle import mode
import sympy as sp
from string import ascii_letters
import streamlit as st  # type: ignore

latters_symbols = (
    "x",
    "y",
    "z",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
)

st.logo(
    "https://t3.ftcdn.net/jpg/05/51/43/56/360_F_551435602_v0rxhHEIgbQNWozIjcgJOR2Nmp1SINMV.jpg"
)
st.title("Maths :blue[cool] :sunglasses:")
st.subheader("This is our first app with Streamlit!")
col_l, col_m, col_r = st.columns(3)

variables = col_l.multiselect("Select the math symbols", latters_symbols)
col_l.write(", ".join(variables))
symb_vars = sp.symbols(", ".join(variables))


expression = st.text_input("Enter your equation here")

st.latex(sp.simplify(expression))


functionality = col_l.selectbox(
    "Select funtionality",
    sorted(["factorize", "expand", "derive", "integrate"]),
        # on change click on submit button
        on_change=lambda: st.session_state.get("btn_submit") == True,
    )

btn_submit = st.button("Submit")
if btn_submit:
    match functionality:
        case "solve":
            sols = sp.solve(expression, sp.symbols(variables, complex=True))
            for sol in sols:
                st.write(f"solution is : {sol}")
        case "factorize":
            st.write(sp.factor(expression))
        case "expand":
            st.write(sp.expand(expression))
        case "derive":
            st.write(sp.diff(expression))
        case "integrate":
            st.write(sp.integrate(expression))
        case _:
            st.write("Wrong input")
