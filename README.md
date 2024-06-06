# pythonCompiler

A compiler made using Python to compile a new language SimpleLang

### 1. **Language Grammar for SimpleLang**
The language SimpleLang supports:
- Two data types: `int` and `float`
- Basic arithmetic operations (`+`, `-`, `*`, `/`) with precedence
- Assignment statements
- Conditional control statements (`IF`)
- Looping control statements (`WHILE`)
- Procedures (functions) with parameters
- Basic error recovery

#### Grammar for SimpleLang

Program     → { Function | Statement }
Function    → 'func' id '(' [Parameters] ')' '{' { Statement } '}'
Parameters  → (Type id { ',' Type id })
Type        → 'int' | 'float'
Statement   → Assignment | IfStatement | WhileStatement | FunctionCall | ';'
Assignment  → id '=' Expression ';'
IfStatement → 'if' '(' Expression ')' '{' { Statement } '}'
WhileStatement → 'while' '(' Expression ')' '{' { Statement } '}'
FunctionCall → id '(' [Arguments] ')' ';'
Arguments   → (Expression { ',' Expression })
Expression  → Term { ('+' | '-') Term }
Term        → Factor { ('*' | '/') Factor }
Factor      → '(' Expression ')' | id | number

### 2. **Compiler Design**

#### Lexical Analysis
The lexical analyzer will tokenize the input source code into tokens.

#### Syntax Analysis
The syntax analyzer (parser) will check the token sequence against the grammar rules and build an abstract syntax tree (AST).

#### Semantic Analysis
This phase will involve type checking and ensuring the semantic correctness of the program.

#### Code Generation
The compiler will generate Python code from the AST, which can be executed.

### 5. **Report**

#### High-Level Description and UML Diagrams

**Classes Overview:**
1. **Token**: Represents tokens in the source code.
2. **Lexer**: Tokenizes the source code.
3. **Parser**: Parses tokens into an AST.
4. **Nodes**: Various AST node types (e.g., ProgramNode, FunctionNode, etc.).
5. **CodeGenerator**: Generates Python code from the AST.

**UML Diagram:**

```plain
+---------------------+
|       Token         |
+---------------------+
| type: TokenType     |
| value: str          |
+---------------------+
          |
          |
          V
+---------------------+
|       Lexer         |
+---------------------+
| tokenize(source: str)
+---------------------+
          |
          |
          V
+---------------------+
|       Parser        |
+---------------------+
| parse(tokens: list) |
+---------------------+
          |
          |
          V
+---------------------+
|       Node          |
+---------------------+
| accept(visitor)     |
+---------------------+
          |
          |
          V
+---------------------+
|   CodeGenerator     |
+---------------------+
| generate(ast: Node) |
+---------------------+
```

#### Grammar for SimpleLang
```plain
Program     → { Function | Statement }
Function    → 'func' id '(' [Parameters] ')' '{' { Statement } '}'
Parameters  → (Type id { ',' Type id })
Type        → 'int' | 'float'
Statement   → Assignment | IfStatement | WhileStatement | FunctionCall | ';'
Assignment  → id '=' Expression ';'
IfStatement → 'if' '(' Expression ')' '{' { Statement } '}'
WhileStatement → 'while' '(' Expression ')' '{' { Statement } '}'
FunctionCall → id '(' [Arguments] ')' ';'
Arguments   → (Expression { ',' Expression })
Expression  → Term { ('+' | '-') Term }
Term        → Factor { ('*' | '/') Factor }
Factor      → '(' Expression ')' | id | number
```

#### Code Templates
- **Lexer**: Tokenizes source code into tokens.
- **Parser**: Parses tokens into AST.
- **Code Generator**: Generates Python code from AST.


### Summary
This project presents the design and implementation of a simple compiler for a custom language called SimpleLang. The compiler handles lexical analysis, syntax analysis, semantic analysis, and code generation, producing executable Python code from SimpleLang source code. The provided report includes a high-level design, grammar specification, and code templates.