from operator import index
from unittest import result
from regex import P
import sympy as sp
from sympy.logic.boolalg import simplify_logic
from sympy.logic.inference import satisfiable, valid, PropKB

# from string import ascii_lowercase
import streamlit as st  # type: ignore

# st.subheader("Logic :blue[cool] :sunglasses:")


# Define symbolic variables
sp_symbols = sp.symbols("P B A W C G")
# P, B, A, W, E, G = sp.symbols('P B A W E G')
all_symbols = [str(symbol) for symbol in sp_symbols]


st.write("### Choose symbols")
# Initialize session state for selectboxes and available options if not exists
if "selectboxes" not in st.session_state:
    st.session_state.selectboxes = []
    selected_symbols = [
        st.session_state[f"select_{i}"]
        for i in range(len(st.session_state.selectboxes))
    ]

if "available_options" not in st.session_state:
    st.session_state.available_options = set(all_symbols) - set(selected_symbols)


# Function to add a new selectbox
def add_selectbox():
    if len(st.session_state.selectboxes) < len(all_symbols):
        st.session_state.available_options = set(all_symbols) - set(selected_symbols)
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
col_symbol, col_sentence, col_check = st.columns(
    [1, 6, 1], gap="small", vertical_alignment="top"
)
for i, options in enumerate(st.session_state.selectboxes):
    selected = col_symbol.selectbox(
        f"Select Symbol {i+1}", sorted(options), key=f"select_{i}"
    )
    sentence = col_sentence.text_input(label=f"Sencence {i+1}", key=f"input_{i}")

    try:
        check_truth = col_check.selectbox(
        f"check {selected}", ["True", "False"], key=f"check_{selected}"
    )
    except :
        pass

# Submit button check if all selected sympbols are unique
selected_symbols = [
    st.session_state[f"select_{i}"] for i in range(len(st.session_state.selectboxes))
]
validites = {
    str(symbol): st.session_state[f"check_{symbol}"] for symbol in selected_symbols
}

if len(st.session_state.selectboxes) >= 1:
    # get non unique symbols in selected_symbols
    if col_symbol.button("CHECK", type="primary"):
        if len(set(selected_symbols)) < len(selected_symbols):
            col_sentence.error("You can't select same symbols twice!")
        else:
            col_sentence.success(f"You selected: {', '.join(selected_symbols)}")
    logical_statement = st.text_area(
        "Write logical Statement",
        help="use '>>' for 'implies', '&' for 'and', '|' for 'or', '~' for 'not'",
    )
    st.write("---")
    if st.button("SOLVE"):
        l:PropKB = PropKB()
        col_sentence, col_result, col_inference = st.columns(
            [2, 1, 4], gap="small", vertical_alignment="top"
        )
        for statement in logical_statement.split("\n"):
            # st.latex(sp.sympify(statement).atoms())
            symp_statement = sp.sympify(statement)
            symp_result = symp_statement.subs(
                {f"{k}": validites[f"{k}"] for k in symp_statement.atoms()}
            )
            col_sentence.latex(sp.latex(symp_statement))
            col_result.latex(symp_result)
            
            simple_statement = simplify_logic(symp_statement, force=True , deep=True)
            satisfiable_result = satisfiable(symp_statement)
            col_inference.latex(satisfiable_result)
            l.tell(simple_statement)

        st.write("---")
        st.write(l.ask(l.clauses[-1]))
            
