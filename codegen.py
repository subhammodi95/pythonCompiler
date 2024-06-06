class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.output = []

    def generate(self):
        self.visit(self.ast)
        self.output.append('main()')
        return '\n'.join(self.output)

    def visit(self, node, indent=0):
        indentation = ' ' * (4 * indent)
        if isinstance(node, ProgramNode):
            for func in node.functions:
                self.visit(func, indent)
        elif isinstance(node, FunctionNode):
            self.output.append(f'{indentation}def {node.name}({", ".join(param[1] for param in node.parameters)}):')
            if not node.body:
                self.output.append(indentation + '    pass')
            for stmt in node.body:
                self.visit(stmt, indent + 1)
        elif isinstance(node, DeclarationNode):
            self.output.append(f'{indentation}{node.var_name} = None')  # Initialize variables as None
        elif isinstance(node, AssignmentNode):
            self.output.append(f'{indentation}{node.variable} = {self.visit(node.expression)}')
        elif isinstance(node, IfNode):
            self.output.append(f'{indentation}if {self.visit(node.condition)}:')
            for stmt in node.body:
                self.visit(stmt, indent + 1)
        elif isinstance(node, WhileNode):
            self.output.append(f'{indentation}while {self.visit(node.condition)}:')
            for stmt in node.body:
                self.visit(stmt, indent + 1)
        # elif isinstance(node, PrintNode):
        #     self.output.append(f'{indentation}print {self.visit(node.body)}:')
        #     for stmt in node.body:
        #         self.visit(stmt, indent + 1)
        elif isinstance(node, FunctionCallNode):
            if node.name == 'print':
                self.output.append(f'{indentation}print({", ".join(self.visit(arg) for arg in node.arguments)})')
            else:
                self.output.append(f'{indentation}{node.name}({", ".join(self.visit(arg) for arg in node.arguments)})')
        elif isinstance(node, ExpressionNode):
            return f'{self.visit(node.left)} {node.operator} {self.visit(node.right)}'
        elif isinstance(node, FactorNode):
            return str(node.value)
        else:
            raise SyntaxError(f"Unsupported node type: {type(node).__name__}")
        

# AST Node Classes
class ProgramNode:
    def __init__(self):
        self.functions = []

class FunctionNode:
    def __init__(self, name):
        self.name = name
        self.parameters = []
        self.body = []

class DeclarationNode:
    def __init__(self, var_type, var_name):
        self.var_type = var_type
        self.var_name = var_name

class AssignmentNode:
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

class IfNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class PrintNode:
    def __init__(self, body):
        self.body = body

class FunctionCallNode:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class ExpressionNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class FactorNode:
    def __init__(self, value):
        self.value = value

