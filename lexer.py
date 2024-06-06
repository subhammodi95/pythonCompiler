#### Tokenizer (Lexical Analyzer)

import re

class TokenType:
    INT = 'INT'
    FLOAT = 'FLOAT'
    ID = 'ID'
    KEYWORD = 'KEYWORD'
    OPERATOR = 'OPERATOR'
    SEPARATOR = 'SEPARATOR'
    EOF = 'EOF'
    UNKNOWN = 'UNKNOWN'

keywords = {'if', 'while', 'func', 'int', 'float'}    #  ,'print'
operators = {'+', '-', '*', '/', '=', '>', '<', '>=', '<=', '==', '!='}
separators = {';', '(', ')', '{', '}', ','}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

def tokenize(source_code):
    token_specification = [
        ('FLOAT',    r'\d+\.\d+'),     # Float number
        ('INT',      r'\d+'),          # Integer number
        ('ID',       r'[A-Za-z_]\w*'), # Identifiers
        ('OPERATOR', r'[\+\-\*/=><!]+'), # Operators
        ('SEPARATOR', r'[;(){}]'),     # Separators
        ('SKIP',     r'[ \t\n]+'),     # Skip whitespace
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    get_token = re.compile(tok_regex).match
    line = source_code
    pos = 0
    tokens = []
    while pos < len(line):
        match = get_token(line, pos)
        if match is not None:
            type = match.lastgroup
            value = match.group(type)
            if type == 'ID' and value in keywords:
                type = 'KEYWORD'
            elif type == 'OPERATOR' and value in operators:
                type = 'OPERATOR'
            elif type == 'SEPARATOR' and value in separators:
                type = 'SEPARATOR'
            elif type == 'SKIP':
                pos = match.end()
                continue
            elif type == 'MISMATCH':
                raise SyntaxError(f'Unexpected character: {value}')
            tokens.append(Token(type, value))
            pos = match.end()
        else:
            raise SyntaxError('Unexpected character at position %d' % pos)
    tokens.append(Token(TokenType.EOF, ''))
    print(tokens)
    return tokens