from narwhals import col
from numpy import real
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
st.subheader("Maths :blue[cool] :sunglasses:")

expr = st.text_input("Enter your expression here")
try:
    expression = sp.sympify(expr)
    st.write(sp.sympify(expression))
    st.write("---")
except:
    st.warning("Write a valide Sympy Expression")
else:
    col_func, col_submit, _ = st.columns(
        [1, 1, 4], gap="small", vertical_alignment="bottom"
    )
    variables = st.sidebar.multiselect(
        "Select the math symbols",
        latters_symbols,
        placeholder="Choose varaible(s)",
    )
    # col_m.write("Choosed varaibles and parameters:")
    if variables == []:
        st.sidebar.warning("Choose at least one variable")
        symb_vars = sp.symbols("x")
    else:
        symb_vars = sp.symbols(" ".join(variables))
        st.sidebar.write(f"variables:", symb_vars)
        
    functionality = col_func.selectbox(
        "Select funtionality",
        sorted(["simplify", "solve", "factorize", "expand", "derive", "integrate"]),
        # on change click on submit button
        on_change=lambda: st.session_state.get("btn_submit") == True,
    )
    # btn_submit = col_submit.write('---')
    btn_submit = col_submit.button("Submit")

    if btn_submit:
        with st.spinner("Calculating..."):
            match functionality:
                case "simplify":
                    result = sp.simplify(expression)
                case "factorize":
                    result = sp.factor(expression)
                case "expand":
                    result = sp.expand(expression)
                case "solve":
                    
                    result = sp.solve(expression, symb_vars)
                case "derive":
                    result = sp.diff(expression, symb_vars).doit(simplify=True)
                case "integrate":
                    result = sp.integrate(expression, symb_vars).doit(simplify=True)
                case _:
                    st.write("Wrong input")
            if isinstance(result, list):
                st.write(f"Solution for {symb_vars}")
                if result == []:
                    st.warning("No solution found")
                for item in result:
                    st.write(sp.simplify(item))
                    # st.write((item))
            else:
                st.write(sp.simplify(result))
