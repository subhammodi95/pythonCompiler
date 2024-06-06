#### Lexical Analysis
#The lexical analyzer will tokenize the input source code into tokens.

#### Syntax Analysis
#The syntax analyzer (parser) will check the token sequence against the grammar rules and build an abstract syntax tree (AST).

#### Semantic Analysis
#This phase will involve type checking and ensuring the semantic correctness of the program.

#### Code Generation
#The compiler will generate Python code from the AST, which can be executed.

### 3. **Compiler Implementation in Python**

from lexer import *
from codegen import *

#### Parser (Syntax Analyzer)




class Node:
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            raise SyntaxError(f"Expected token {token_type}, got {self.current_token.type}")

    def parse(self):
        program = ProgramNode()
        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == 'KEYWORD' and self.current_token.value == 'func':
                program.functions.append(self.function())
            else:
                raise SyntaxError(f"Unexpected token {self.current_token.type}")
        return program

    def function(self):
        self.eat('KEYWORD')  # 'func'
        name = self.current_token.value
        self.eat('ID')
        self.eat('SEPARATOR')  # '('
        parameters = self.parameters()
        self.eat('SEPARATOR')  # ')'
        self.eat('SEPARATOR')  # '{'
        body = self.statements()
        self.eat('SEPARATOR')  # '}'
        func = FunctionNode(name)
        func.parameters = parameters
        func.body = body
        return func

    def parameters(self):
        parameters = []
        while self.current_token.type != 'SEPARATOR' or self.current_token.value != ')':
            type = self.current_token.value
            self.eat('KEYWORD')
            name = self.current_token.value
            self.eat('ID')
            parameters.append((type, name))
            if self.current_token.type == 'SEPARATOR' and self.current_token.value == ',':
                self.eat('SEPARATOR')
        return parameters

    def statements(self):
        statements = []
        while self.current_token.type != 'SEPARATOR' or self.current_token.value != '}':
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token.type == 'ID':
            if self.lookahead().type == 'OPERATOR' and self.lookahead().value == '=':
                return self.assignment()
            elif self.lookahead().type == 'SEPARATOR' and self.lookahead().value == '(':
                return self.function_call()
        elif self.current_token.type == 'KEYWORD':
            if self.current_token.value in {'int', 'float'}:
                return self.declaration()
            elif self.current_token.value == 'if':
                return self.if_statement()
            elif self.current_token.value == 'while':
                return self.while_statement()
            # elif self.current_token.value == 'print':
            #     return self.print_statement()
        raise SyntaxError(f"Unexpected statement {self.current_token.value}")

    def lookahead(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return Token(TokenType.EOF, '')

    def assignment(self):
        variable = self.current_token.value
        self.eat('ID')
        self.eat('OPERATOR')  # '='
        expression = self.expression()
        self.eat('SEPARATOR')  # ';'
        return AssignmentNode(variable, expression)

    def declaration(self):
        var_type = self.current_token.value
        self.eat('KEYWORD')
        var_name = self.current_token.value
        self.eat('ID')
        self.eat('SEPARATOR')  # ';'
        return DeclarationNode(var_type, var_name)

    def if_statement(self):
        self.eat('KEYWORD')  # 'if'
        self.eat('SEPARATOR')  # '('
        condition = self.expression()
        self.eat('SEPARATOR')  # ')'
        self.eat('SEPARATOR')  # '{'
        body = self.statements()
        self.eat('SEPARATOR')  # '}'
        return IfNode(condition, body)

    def while_statement(self):
        self.eat('KEYWORD')  # 'while'
        self.eat('SEPARATOR')  # '('
        condition = self.expression()
        self.eat('SEPARATOR')  # ')'
        self.eat('SEPARATOR')  # '{'
        body = self.statements()
        self.eat('SEPARATOR')  # '}'
        return WhileNode(condition, body)
    
    # def print_statement(self):
    #     self.eat('KEYWORD')  # 'print'
    #     self.eat('SEPARATOR')  # '('
    #     body = self.statements()
    #     self.eat('SEPARATOR')  # ')'
    #     self.eat('SEPARATOR')  # ';'
    #     return PrintNode(body)


    def function_call(self):
        name = self.current_token.value
        self.eat('ID')
        self.eat('SEPARATOR')  # '('
        arguments = []
        if self.current_token.type != 'SEPARATOR' or self.current_token.value != ')':
            arguments = self.arguments()
        self.eat('SEPARATOR')  # ')'
        self.eat('SEPARATOR')  # ';'
        return FunctionCallNode(name, arguments)

    def arguments(self):
        arguments = []
        arguments.append(self.expression())
        while self.current_token.type == 'SEPARATOR' and self.current_token.value == ',':
            self.eat('SEPARATOR')
            arguments.append(self.expression())
        return arguments

    def expression(self):
        node = self.term()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in ('+', '-', '>', '<', '>=', '<=', '==', '!='):
            operator = self.current_token.value
            self.eat('OPERATOR')
            node = ExpressionNode(node, operator, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in ('*', '/'):
            operator = self.current_token.value
            self.eat('OPERATOR')
            node = ExpressionNode(node, operator, self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == 'SEPARATOR' and token.value == '(':
            self.eat('SEPARATOR')
            node = self.expression()
            self.eat('SEPARATOR')  # ')'
            return node
        elif token.type in ('INT', 'FLOAT', 'ID'):
            self.eat(token.type)
            return FactorNode(token.value)
        else:
            raise SyntaxError(f"Unexpected token {token.type}")
        
    
    def print_ast(self, node, indent=0):
        indentation = ' ' * (2 * indent)
        if isinstance(node, ProgramNode):
            print(f'{indentation}ProgramNode')
            for func in node.functions:
                self.print_ast(func, indent + 1)
        elif isinstance(node, FunctionNode):
            print(f'{indentation}FunctionNode(name={node.name})')
            for param in node.parameters:
                print(f'{indentation}  Parameter(type={param[0]}, name={param[1]})')
            for stmt in node.body:
                self.print_ast(stmt, indent + 1)
        elif isinstance(node, DeclarationNode):
            print(f'{indentation}DeclarationNode(type={node.var_type}, name={node.var_name})')
        elif isinstance(node, AssignmentNode):
            print(f'{indentation}AssignmentNode(variable={node.variable})')
            self.print_ast(node.expression, indent + 1)
        elif isinstance(node, IfNode):
            print(f'{indentation}IfNode')
            self.print_ast(node.condition, indent + 1)
            for stmt in node.body:
                self.print_ast(stmt, indent + 1)
        elif isinstance(node, WhileNode):
            print(f'{indentation}WhileNode')
            self.print_ast(node.condition, indent + 1)
            for stmt in node.body:
                self.print_ast(stmt, indent + 1)
        elif isinstance(node, FunctionCallNode):
            print(f'{indentation}FunctionCallNode(name={node.name})')
            for arg in node.arguments:
                self.print_ast(arg, indent + 1)
        elif isinstance(node, ExpressionNode):
            print(f'{indentation}ExpressionNode(operator={node.operator})')
            self.print_ast(node.left, indent + 1)
            self.print_ast(node.right, indent + 1)
        elif isinstance(node, FactorNode):
            print(f'{indentation}FactorNode(value={node.value})')



# =============================
source_code = """
func main() {
    int a;
    float b;
    a = 5;
    b = 3.14;
    if (c > b) {
        a = a - 1;
    }
    while (a < 10){
        a = a + 1;
    }
    print(a);
}
"""

tokens = tokenize(source_code)
parser = Parser(tokens)
ast = parser.parse()
parser.print_ast(ast) 
generator = CodeGenerator(ast)
python_code = generator.generate()
print("python code")
print(python_code)
exec(python_code)

