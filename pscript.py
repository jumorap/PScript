import ply.lex as lex
import ply.yacc as yacc
import numpy as np
import alghtms as alg
import sys


reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
    'sqrt': 'SQRT',
    'arcsin': 'ARCSIN',
    'arccos': 'ARCCOS',
    'arctan': 'ARCTAN',
    'abs': 'ABS',
    'floor': 'FLOOR',
    'round': 'ROUND',
    'ceil': 'CEIL',
    'print': 'PRINT',
    'and': 'AND',
    'or': 'OR',
    'true': 'TRUE',
    'false': 'FALSE',
    'function': 'FUNCTION',
    'call': 'CALL',
    'len': 'LEN',
    'model': 'MODEL',
    'chain': 'CHAIN',
    'printm': 'PRINTM',
    'plot': 'PLOT',
}

# Create a list to hold all of the token names
tokens = [
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'POWER',
    'GTE',
    'LTE',
    'GT',
    'LT',
    'NE',
    'EQ',
    'SEMICOLON',
    'DOT',
]

tokens = tokens + list(reserved.values())

# Use regular expressions to define what each token is
t_GTE = r'>='
t_LTE = r'<='
t_GT = r'>'
t_LT = r'<'
t_NE = r'!='
t_EQ = r'=='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_POWER = r'\^'
t_EQUALS = r'\='

t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'


# Define a rule so we can track line numbers
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


# Ply's special t_ignore variable allows us to define characters the lexer will ignore.
# We're ignoring spaces.
t_ignore = r' '


# More complicated tokens, such as tokens that are more than 1 character in length
# are defined using functions.
# A float is 1 or more numbers followed by a dot (.) followed by 1 or more numbers again.
def t_FLOAT(t):
    r"""-?\d+\.\d+"""
    t.value = float(t.value)
    return t


# An int is 1 or more numbers.
def t_INT(t):
    r"""-?\d+"""
    t.value = int(t.value)
    return t


# A NAME is a variable name. A variable can be 1 or more characters in length.
# The first character must be in the ranges a-z A-Z or be an underscore.
# Any character following the first character can be a-z A-Z 0-9 or an underscore.
def t_NAME(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    if t.value in reserved:
        t.type = reserved[t.value]
    else:
        t.type = 'NAME'
    return t


# Skip the current token and output 'Illegal characters' using the special Ply t_error function.
def t_error(t):
    print(f"Lexical error found: Illegal character '{t.value[0]}' in line {t.lineno}")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Ensure our parser understands the correct order of operations.
# The precedence variable is a special Ply variable.
precedence = (
    ('left', 'OR', 'AND'),
    ('left', 'GTE', 'LTE', 'GT', 'LT', 'NE', 'EQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'POWER'),
)


def p_code(p):
    """
    code : if_expression
            | block
    """
    for i in p[1][1]:
        run(i)


def p_while_statement(p):
    """
    while_statement : WHILE LPAREN expression RPAREN LBRACE block RBRACE
    """
    p[0] = ("while", p[3], p[6])


def p_if_statement(p):
    """
    if_expression : IF LPAREN expression RPAREN LBRACE block RBRACE
    | IF LPAREN expression RPAREN LBRACE block RBRACE ELSE LBRACE block RBRACE
    """
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('if', p[3], p[6], p[10])


def p_function_declaration(p):
    """
    function_declaration : FUNCTION  NAME LPAREN function_parameters RPAREN LBRACE block RBRACE
    """
    p[0] = ("function_declaration", p[2], p[4], p[7])


def p_function_call(p):
    """
    function_call : CALL NAME LPAREN function_parameters RPAREN
    """
    p[0] = ("function_call", p[2], p[4])


def p_function_parameters(p):
    """
    function_parameters : NAME
                        | NAME COMMA function_parameters
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_array_get(p):
    """
    expression : NAME LBRACKET expression RBRACKET
    """
    p[0] = ("array_get", p[1], p[3])


def p_block(p):
    """
    block :  line block
            | line
    """
    if len(p) == 2:
        p[0] = ("block", [p[1]])
    else:
        p[0] = ("block", [p[1]] + p[2][1])


def p_line(p):
    """
    line : expression SEMICOLON
         | var_assign SEMICOLON
         | function_print SEMICOLON
         | if_expression SEMICOLON
         | while_statement SEMICOLON
         | function_declaration SEMICOLON
         | function_call SEMICOLON
         | model SEMICOLON
         | chain SEMICOLON
         | function_plot SEMICOLON
    """
    p[0] = p[1]


def p_primt_message(p):
    """
    function_print : PRINTM LPAREN NAME RPAREN
    """
    p[0] = ("printm", p[3])


def p_plot(p):
    """
    function_plot : PLOT LPAREN expression COMMA NAME RPAREN
    """
    p[0] = ("plot", p[3], p[5])


def p_function_print(p):
    """
    function_print : PRINT LPAREN expression RPAREN
    """
    p[0] = ('print', p[3])


def p_array(p):
    """
    expression : LBRACKET array_elements RBRACKET
    """
    new_array = []
    new_array.extend(p[2])
    p[0] = new_array


def p_array_elements(p):
    """
    array_elements : array_elements COMMA expression
                   | expression
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_len(p):
    """
    expression : LEN LPAREN expression RPAREN
    """
    p[0] = ("len", p[3])


def p_var_assign(p):
    """
    var_assign : NAME EQUALS expression
                 | NAME EQUALS model
                 | NAME EQUALS chain
    """
    # Build our tree
    p[0] = ('=', p[1], p[3])


def p_declare_mode(p):
    """
    model : MODEL LPAREN NAME COMMA NAME COMMA NAME COMMA NAME RPAREN
    """
    p[0] = ("model", ('var', p[3]), ('var', p[5]), ('var', p[7]), ('var', p[9]))


def p_model_operations(p):
    """
    expression : NAME DOT NAME LPAREN model_parameters RPAREN
    """
    # p[3] = name of the function
    # p[1] = name of the objetc
    # p[5] = parameters
    p[0] = (p[3], p[1], p[5])


def p_model_parameters(p):
    """
    model_parameters : string
                     | string COMMA model_parameters
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_string(p):
    """
    string : NAME
           | DOT
           | INT
           | empty
    """
    if p[1] is None:
        p[0] = None
    elif type(p[1]) == int:
        p[0] = p[1]
    elif str.isdigit(p[1]):
        p[0] = int(p[1])
    elif p[1] == '.':
        p[0] = '.'
    elif p[1] == 'empty':
        p[0] = ''
    else:
        p[0] = ("var", p[1])


def p_declare_chain(p):
    """
    chain : CHAIN LPAREN NAME RPAREN
    """
    p[0] = ("chain", p[3])


def p_expression_function(p):
    """
    expression : SIN LPAREN expression RPAREN
                | COS LPAREN expression RPAREN
                | TAN LPAREN expression RPAREN
                | SQRT LPAREN expression RPAREN
                | ARCSIN LPAREN expression RPAREN
                | ARCCOS LPAREN expression RPAREN
                | ARCTAN LPAREN expression RPAREN
                | ABS LPAREN expression RPAREN
                | FLOOR LPAREN expression RPAREN
                | ROUND LPAREN expression RPAREN
                | CEIL LPAREN expression RPAREN

    """
    p[0] = (p[1], p[3])


# Expressions are recursive.
def p_expression(p):
    """
    expression : expression MULTIPLY expression
                | expression DIVIDE expression
                | expression PLUS expression
                | expression MINUS expression
                | expression POWER expression
                | expression GTE expression
                | expression LTE expression
                | expression GT expression
                | expression LT expression
                | expression EQ expression
                | expression NE expression
                | expression AND expression
                | expression OR expression
    """
    # Build our tree.
    p[0] = (p[2], p[1], p[3])


def p_expression_int_float(p):
    """
    expression : INT
               | FLOAT
    """
    p[0] = p[1]


def p_expression_bool(p):
    """
    expression : TRUE
               | FALSE
    """
    if p[1] == 'true':
        p[0] = True
    else:
        p[0] = False


def p_expression_var(p):
    """
    expression : NAME
    """
    p[0] = ('var', p[1])


def p_error(p):
    """
    Output to the user that there is an error in the input as it doesn't conform to our grammar.
    p_error is another special Ply function.
    :param p: The input that doesn't conform to our grammar.
    """
    print("Syntax error found: ", p)


def p_empty(p):
    """
    empty :
    """
    p[0] = None


parser = yacc.yacc()  # Build the parser
env = {}  # Create the environment upon which we will store and retrieve variables from.
small_env = {}  # Create the function environment upon which we will store and retrieve functions from.


def run(p):
    """
    The run function is our recursive function that 'walks' the tree generated by our parser.
    :param p: The tree generated by our parser.
    :return: The result of the tree.
    """
    global env
    if type(p) == tuple:
        if p[0] == '+':
            left = run(p[1])
            right = run(p[2])
            if type(left) == list:
                left = np.array(left)
            if type(right) == list:
                right = np.array(right)
            return left + right
        elif p[0] == '-':
            left = run(p[1])
            right = run(p[2])
            if type(left) == list:
                left = np.array(left)
            if type(right) == list:
                right = np.array(right)
            return left - right
        elif p[0] == '*':
            left = run(p[1])
            right = run(p[2])
            if type(left) == list:
                left = np.array(left)
            if type(right) == list:
                right = np.array(right)
            return left * right
        elif p[0] == '/':
            left = run(p[1])
            right = run(p[2])
            if type(left) == list:
                left = np.array(left)
            if type(right) == list:
                right = np.array(right)
            return left / right
        elif p[0] == 'sin':
            return np.sin(run(p[1]))
        elif p[0] == 'cos':
            return np.cos(run(p[1]))
        elif p[0] == 'tan':
            return np.tan(run(p[1]))
        elif p[0] == 'sqrt':
            return np.sqrt(run(p[1]))
        elif p[0] == 'arcsin':
            return np.arcsin(run(p[1]))
        elif p[0] == 'arccos':
            return np.arccos(run(p[1]))
        elif p[0] == 'arctan':
            return np.arctan(run(p[1]))
        elif p[0] == 'abs':
            return np.abs(run(p[1]))
        elif p[0] == 'floor':
            return np.floor(run(p[1]))
        elif p[0] == 'round':
            return np.round(run(p[1]))
        elif p[0] == 'ceil':
            return np.ceil(run(p[1]))
        elif p[0] == '^':
            return run(p[1]) ** run(p[2])
        elif p[0] == '>=':
            return run(p[1]) >= run(p[2])
        elif p[0] == '<=':
            return run(p[1]) <= run(p[2])
        elif p[0] == '>':
            return run(p[1]) > run(p[2])
        elif p[0] == '<':
            return run(p[1]) < run(p[2])
        elif p[0] == '==':
            return run(p[1]) == run(p[2])
        elif p[0] == 'and':
            return run(p[1]) and run(p[2])
        elif p[0] == 'or':
            return run(p[1]) or run(p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])
        elif p[0] == 'print':
            print(run(p[1]))
        elif p[0] == 'array_get':
            return env[p[1]][run(p[2])]
        elif p[0] == 'len':
            return int(len(run(p[1])))
        elif p[0] == 'model':
            return alg.Model(run(p[1]), run(p[2]), run(p[3]), run(p[4]))
        elif p[0] == 'operationNum':
            # p[0] = name of the function
            # p[1] = name of the objetc
            # p[2] = parameters
            if p[1] not in env:
                print(f'Error: object {p[1]} is not defined')
                return
            return env[p[1]].operationNum(run(p[2][0]), run(p[2][1]))
        elif p[0] == 'operationSet':
            if p[1] not in env:
                print(f'Error: object {p[1]} is not defined')
                return
            return env[p[1]].operationSet(run(p[2][0]), run(p[2][1]))
        elif p[0] == 'toStreakModel':
            if p[1] not in env:
                print(f'Error: object {p[1]} is not defined')
                return
            return env[p[1]].toSteakModel()
        elif p[0] == 'steakOperationSum':
            if p[1] not in env:
                print(f'Error: object {p[1]} is not defined')
                return
            return env[p[1]].steakOperationSum(run(p[2][0]), run(p[2][1]), run(p[2][2]))
        elif p[0] == 'SteakOperationAvrg':
            if p[1] not in env:
                print(f'Error: object {p[1]} is not defined')
                return
            return env[p[1]].SteakOperationAvrg(run(p[2][0]), run(p[2][1]), run(p[2][2]))
        elif p[0] == 'chain':
            return alg.Chain(p[1])

        elif p[0] == 'numberOfSteaks':
            if p[1] not in env:
                print(f'Error: object {p[1]} is not defined')
                return
            return env[p[1]].numberOfSteaks()

        elif p[0] == 'numberOfSteaksUntilIndex':
            if p[1] not in env:
                print(f'Error: object {p[1]} is not defined')
                return
            return env[p[1]].numberOfSteaksUntilIndex(p[2][0])
        elif p[0] == 'printm':
            print(">>", p[1])
        elif p[0] == 'plot':
            if type(p[1]) == "str" and p[1] not in env:
                print(f'Error: object {p[1]} is not defined')
                return
            alg.showPlot(run(p[1]), run(p[2]))
        elif p[0] == 'function_declaration':
            # p2 are the arguments of the function
            # p3 are the statements of the function
            env[p[1]] = ("function", p[2], p[3])
        elif p[0] == 'function_call':
            # p2 is the name of the function
            # p3 are the arguments of the function
            name = p[1]
            args = p[2]
            if name not in env:
                print("Function not found: ", name)
                return None

            function_values = env[name]
            # function_values[1] are the arguments of the function
            # function_values[2] are the statements of the function
            if function_values[0] != "function":
                print("Not a function: ", name)
                return None
            if len(function_values[1]) != len(args):
                print("Argument count mismatch, the function requires ", len(function_values[1]),
                      " arguments but you supplied ", len(args))
                return None
            # Add the arguments to the new environment
            for i in range(len(args)):
                env[function_values[1][i]] = env[args[i]]
            run(function_values[2])
        elif p[0] == 'if':
            if run(p[1]):
                return run(p[2])
            else:
                if len(p) > 3:
                    return run(p[3])
        elif p[0] == 'block':
            for x in p[1]:
                run(x)
        elif p[0] == 'while':
            while run(p[1]):
                run(p[2])
        elif p[0] == 'var':
            if p[1] not in env:
                return 'Undeclared variable found!' + p[1]
            else:
                return env[p[1]]
    else:
        return p


def exe(tokenize=False, file_name=None):
    """
    Receives the input from the user and executes the code
    If the user enters a file name, it will execute the code in the file
    If the user not, it will execute the code through the terminal
    """
    if file_name:
        with open(file_name) as f:
            code = f.read()

        if not tokenize:
            parser.parse(code)
        else:
            lexer.input(code)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok)
    else:
        while True:
            try:
                s = input('Sigma>> ')
            except EOFError:
                break
            if not tokenize:
                parser.parse(s)
            else:
                lexer.input(s)
                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    print(tok)


def main():
    """
    The full execution case looks like: py pscript.py filename -t
    filename argument is optional: if it is not given, the program will run in the terminal
    tokenize argument is optional: if it is not given, default value is False

    There are 4 possible cases:
    1. py pscript.py filename -t
    2. py pscript.py filename
    3. py pscript.py -t
    4. py pscript.py
    """
    if len(sys.argv) == 3:
        exe(tokenize=True, file_name=sys.argv[1])
    elif len(sys.argv) == 2:
        if sys.argv[1] == "-t":
            exe(tokenize=True)
        else:
            exe(file_name=sys.argv[1])
    else:
        exe()


if __name__ == "__main__":
    main()
