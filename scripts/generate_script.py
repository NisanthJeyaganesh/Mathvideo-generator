import ast
import operator as op

# Supported operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos

}

def eval_expr(expr):
    """
    Safely evaluate a mathematical expression using AST.
    Supports +, -, *, /, **, %, unary +/-
    """
    def _eval(node):
        if isinstance(node, ast.Num):  # Python < 3.8
            print(f"📦 Num: {node.n}")
            return node.n
        elif isinstance(node, ast.Constant):  # Python >= 3.8
            print(f"📦 Constant: {node.value}")
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Only numeric constants are allowed.")
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            print(f"🧮 BinaryOp: {left} {type(node.op).__name__} {right}")
            if type(node.op) in operators:
                return operators[type(node.op)](left, right)
            else:
                raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            print(f"🔁 UnaryOp: {type(node.op).__name__}{operand}")
            if type(node.op) in operators:
                return operators[type(node.op)](operand)
            else:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        else:
            raise ValueError(f"Unsupported expression node: {type(node).__name__}")

    try:
        tree = ast.parse(expr, mode='eval')
        print(f"🌲 Parsed AST: {ast.dump(tree)}")
        return _eval(tree.body)
    except SyntaxError as se:
        raise ValueError(f"Invalid syntax: {se}")
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}")

def generate_script(prompt):
    prompt = prompt.strip()

    if not prompt:
        return ""

    try:
        result = eval_expr(prompt)
        return f"{prompt} = {result}"
    except Exception as e:
        return f"❗ Could not compute the expression: {prompt} ({e})"
