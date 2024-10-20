from operator import index
from unittest import result
import sympy as sp
import sympy.logic as logic
from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent, to_cnf
from sympy.logic.inference import satisfiable, valid, PropKB

# from string import ascii_lowercase
import streamlit as st  # type: ignore

# st.subheader("Logic :blue[cool] :sunglasses:")


# Define symbolic variables
all_symbols = sp.symbols("O B A")
# P, B, A, W, E, G = sp.symbols('P B A W E G')
all_symbols = [str(symbol) for symbol in sp.symbols("A B C D")]


# # Define logical statements
# # 1. O ⇒ A (Omnipotence implies ability)
# st.write("### Choose symbols")
# col_symbol, col_sentence = st.columns([2, 6], gap="small", vertical_alignment="top")
# s, p = [], []
# proposition = dict()
# for i, symbol in enumerate(all_symbols):
#     s.append(col_symbol.selectbox("", set(all_symbols) - set(s), key=symbol))
#     p.append(col_sentence.text_input("", value="Omnipotence", key=i))
#     # proposition[s[i]] = col_result.checkbox("True", key=i+100, value=True)
# # s2 = col_symbol.selectbox("", set(all_symbols) - {s1})
# # prop2 = col_sentence.text_input("", value="ability")

# st.write("---")
# st.write("### Build Rules")


# stmt1 = ((s[0] >> s[1]) & s[2]) & s[3]
# col_symbol.latex(sp.latex(stmt1))
# col_sentence.text(f"{p[0]} ⇒ {p[1]}")
# col_sentence.text(stmt1.subs({f"{k}": proposition[k] for k in stmt1.atoms()}))
# st.write({f"{k}": proposition[k] for k in stmt1.atoms()})


st.title("Dynamic Selectbox Letter Chooser")
# Initialize session state for selectboxes and available options if not exists
if "selectboxes" not in st.session_state:
    st.session_state.selectboxes = []
    selected_letters = [
        st.session_state[f"select_{i}"]
        for i in range(len(st.session_state.selectboxes))
    ]

if "available_options" not in st.session_state:
    st.session_state.available_options = set(all_symbols) - set(selected_letters)


# Function to add a new selectbox
def add_selectbox():
    if len(st.session_state.selectboxes) < len(all_symbols):
        st.session_state.available_options = set(all_symbols) - set(selected_letters)
        st.session_state.selectboxes.append(tuple(st.session_state.available_options))


# Function to remove the last selectbox
def remove_selectbox():
    if len(st.session_state.selectboxes) > 1:
        removed_option = st.session_state[
            f"select_{len(st.session_state.selectboxes) - 1}"
        ]
        st.session_state.available_options.add(removed_option)
        st.session_state.selectboxes.pop()


# Add and Remove buttons
col1, col2 = st.columns(2)
with col1:
    st.button("Add Selectbox", on_click=add_selectbox)
with col2:
    st.button("Remove Selectbox", on_click=remove_selectbox)
# Display selectboxes
for i, options in enumerate(st.session_state.selectboxes):
    selected = st.selectbox(f"Select letter {i+1}", sorted(options), key=f"select_{i}")

# Submit button and display selected letters
selected_letters = [
    st.session_state[f"select_{i}"] for i in range(len(st.session_state.selectboxes))
]
if st.button("Submit"):
    st.success(f"You selected: {', '.join(selected_letters)}")
