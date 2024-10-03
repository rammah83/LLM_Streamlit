import sympy as sp
from string import ascii_lowercase
import streamlit as st  # type: ignore

latters_symbols = list(ascii_lowercase)

st.logo(
    r".\res\img\mylogo.jpeg",
)
st.subheader("Maths :blue[cool] :sunglasses:")

expr = st.text_input("Enter your expression here")
try:
    expression = sp.sympify(expr)
    st.write(expression)
    st.write("---")
except:
    st.warning("Write a valide Sympy Expression")
else:
    col_func, col_submit, _ = st.columns(
        [1, 1, 4], gap="small", vertical_alignment="bottom"
    )
    variables_symbols:set = expression.free_symbols
    symb_vars = st.sidebar.multiselect(
        label="Select the math symbols",
        options=variables_symbols,
        default=next(iter(variables_symbols)),
        placeholder="Choose varaible(s)",
    )
    # col_m.write("Choosed varaibles and parameters:")
    if symb_vars == []:
        st.sidebar.warning("Choose at least one variable")
        # symb_vars = sp.symbols("x", integer=True)
    else:
        st.sidebar.write(f"variables:", ' '.join(str(symb_vars)))
        

    functionality = col_func.selectbox(
        "Select funtionality",
        sorted(["simplify", "factorize", "expand", "limit", "solve", "derive", "integrate"]),
        # on change click on submit button
        on_change=lambda: st.session_state.get("btn_submit") == True,
    )
    # btn_submit = col_submit.write('---')
    btn_submit = col_submit.button("Submit")

    if btn_submit:
        with st.spinner("Calculating..."):
            match functionality:
                # basic
                case "simplify":
                    result = sp.simplify(expression)
                    st.write(result)
                case "factorize":
                    result = sp.factor(expression)
                    st.write(result)
                case "expand":
                    result = sp.expand(expression)
                    st.write(result)
                # advanced           
                case "limit":
                    st.latex(sp.latex(f"limit({expression}), {symb_vars[0]} --> oo)"))
                    result = sp.limit(expression, symb_vars[0], symb_vars[1])
                    st.write(result)          
                case "solve":
                    result = sp.solve(expression, symb_vars)
                    if result == []:
                        st.warning("No solution found")
                    else:
                        st.write(f"Solution for {symb_vars}")
                        for item in result:
                            st.write(sp.simplify(item))
                case "derive":
                    result = sp.diff(expression, symb_vars).doit(simplify=True)
                case "integrate":
                    result = sp.integrate(expression, symb_vars).doit(simplify=True)
                case _:
                    st.write("Wrong input")
