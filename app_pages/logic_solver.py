from sympy import symbols, latex
import sympy.logic as logic
from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent
# from string import ascii_lowercase
import streamlit as st  # type: ignore

st.subheader("Logic :blue[cool] :sunglasses:")



# Define symbolic variables
O, B, A, W, E, G = symbols('O B A W E G')


# Define logical statements
# 1. O ⇒ A (Omnipotence implies ability)
col_symbol, col_sentence, col_result = st.columns([1,3, 1], gap="small")

s1 = col_symbol.selectbox("Choose symbols 1", ["O", "B", "A", "W", "E", "G"])
col_sentence.text_input("Enter sentence", value="Omnipotence")

s2 = col_symbol.selectbox("Choose symbols 2", ["O", "B", "A", "W", "E", "G"])
col_sentence.text_input("Enter sentence", value="ability")

stmt1 = Implies(O, A)
st.latex(stmt1)