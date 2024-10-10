from operator import index
from unittest import result
import sympy as sp
import sympy.logic as logic
from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent, to_cnf
from sympy.logic.inference import satisfiable, valid, PropKB
# from string import ascii_lowercase
import streamlit as st  # type: ignore

st.subheader("Logic :blue[cool] :sunglasses:")



# Define symbolic variables
all_symbols = sp.symbols('O B A W')
# P, B, A, W, E, G = sp.symbols('P B A W E G')


# Define logical statements
# 1. O ⇒ A (Omnipotence implies ability)
st.write("Choose symbols")
col_symbol, col_result,  col_sentence = st.columns([2, 1, 6], gap="small", vertical_alignment="center")
s, p = [], []
proposition = dict()
for i, symbol in enumerate(all_symbols):
    s.append(col_symbol.selectbox("", set(all_symbols) - set(s), key=symbol))
    p.append(col_sentence.text_input("", value="Omnipotence", key=i))
    proposition[s[i]] = col_result.checkbox("True", key=i+100, value=True)
# s2 = col_symbol.selectbox("", set(all_symbols) - {s1})
# prop2 = col_sentence.text_input("", value="ability")

st.write("---")
stmt1 = ((s[0] >> s[1]) & s[2]) & s[3] 
col_symbol.latex(sp.latex(stmt1))
col_sentence.text(f"{p[0]} ⇒ {p[1]}")
col_sentence.text(stmt1.subs({f"{k}": proposition[k] for k in stmt1.atoms()}))
st.write({f"{k}": proposition[k] for k in stmt1.atoms()})