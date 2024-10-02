import sympy as sp


def sympy_to_latex_raw(expression):
    """
    Convert a SymPy expression to LaTeX and return it as a raw string.

    Args:
    expression (sympy.Expr): A SymPy expression

    Returns:
    str: LaTeX representation of the expression as a raw string
    """
    # Convert the SymPy expression to LaTeX
    latex_expr = sp.latex(expression)

    # Convert the LaTeX string to a raw string
    raw_latex = r"{}".format(latex_expr)

    return raw_latex


# Example usage:
if __name__ == "__main__":
    # Create a sample SymPy expression
    x, y = sp.symbols("x y")
    expr = sp.sqrt(x**2 + y**2)

    # Convert the expression to LaTeX raw string
    result = sympy_to_latex_raw(expr)

    print("Original expression:", expr)
    print("LaTeX raw string:", result)

# Created/Modified files during execution:
# No files were created or modified during the execution of this code.
