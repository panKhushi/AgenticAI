import ast
import operator as op
import math

OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "abs": abs,
    "round": round,
}


def calculator(expression: str):
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)

        # Generate a proper response
        response = _generate_response(tree.body, result)
        return response

    except Exception as e:
        return f"Calculator Error: {e}"


def execute(arguments: dict):
    """
    Entry point used by the tool registry.
    """
    expression = arguments.get("expression")

    if not expression:
        return "Calculator Error: No expression provided."

    return calculator(expression)


def _evaluate(node):

    if isinstance(node, ast.Constant):
        return node.value

    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right)
        )

    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.operand)
        )

    elif isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")

        func_name = node.func.id

        if func_name not in FUNCTIONS:
            raise ValueError(f"Unsupported function: {func_name}")

        args = [_evaluate(arg) for arg in node.args]

        return FUNCTIONS[func_name](*args)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def _generate_response(node, result):
    """Return a human-readable sentence."""

    if isinstance(node, ast.BinOp):

        if isinstance(node.op, ast.Add):
            return f"The sum is {result}."

        elif isinstance(node.op, ast.Sub):
            return f"The difference is {result}."

        elif isinstance(node.op, ast.Mult):
            return f"The product is {result}."

        elif isinstance(node.op, ast.Div):
            return f"The quotient is {result}."

        elif isinstance(node.op, ast.Pow):
            return f"The result of the exponentiation is {result}."

        elif isinstance(node.op, ast.Mod):
            return f"The remainder is {result}."

    elif isinstance(node, ast.Call):
        func_name = node.func.id

        if func_name == "sqrt":
            return f"The square root is {result}."

        elif func_name == "sin":
            return f"The sine value is {result}."

        elif func_name == "cos":
            return f"The cosine value is {result}."

        elif func_name == "tan":
            return f"The tangent value is {result}."

        elif func_name == "abs":
            return f"The absolute value is {result}."

        elif func_name == "round":
            return f"The rounded value is {result}."

    return f"The result is {result}."


if __name__ == "__main__":

    print(execute({"expression": "5+6"}))
    print(execute({"expression": "25*18"}))
    print(execute({"expression": "(245+89)/2"}))
    print(execute({"expression": "sqrt(625)"}))
    print(execute({"expression": "2**5"}))