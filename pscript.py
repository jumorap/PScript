import ply.lex as lex
import ply.yacc as yacc
from colorama import init, Fore, Style
import numpy as np
import signal
import sys

import algorithms_py.alghtms as alg
import algorithms_py.rand as lcg_rand
import execution

init()

# Reserved words
# VARNAMES that aren't reserved words are considered to be variables.
# VARNAMES that aren't reserved words but are used in the language are called NAMES.
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
    'fun': 'FUN',
    'call': 'CALL',
    'len': 'LEN',
    'model': 'MODEL',
    'chain': 'CHAIN',
    'printm': 'PRINTM',
    'plot': 'PLOT',
    'plotHist': 'PLOTHIST',
    'append': 'APPEND',
}

# Create a list to hold all the token names
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
    'POWER',  # Exponentiation
    'GTE',  # Greater than or equal to
    'LTE',  # Less than or equal to
    'GT',  # Greater than
    'LT',  # Less than
    'NE',  # Not equal to
    'EQ',  # Equal to
    'SEMICOLON',
    'DOT',
    'STRING',
]

tokens = tokens + list(reserved.values())

# Use regular expressions to define what each token is
# TOKEN GENERATORS
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

# Ply's special t_ignore variable allows us to define characters the lexer will ignore.
# We're ignoring spaces.
t_ignore = r' '


# Define a rule so we can track line numbers
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


# Skip the current token and output 'Illegal characters' using the special Ply t_error function.
def t_error(t):
    print(Fore.RED + f"Lexical error found: Illegal character '{t.value[0]}' in line {t.lineno}" + Style.RESET_ALL)
    t.lexer.skip(1)


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


# A string is a sequence of characters surrounded by double quotes.
# We remove the quotes from the string before returning it.
def t_STRING(t):
    r"""\".*\""""
    t.value = t.value[1:-1]  # Remove the quotes from the string
    return t


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


# THE SYNTAX RULES FOR THE GRAMMAR ARE DEFINED HERE
# Grammar is a set of rules and norms that define the structure and correct usage of words, phrases,
# and expressions in a specific language.
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
    # WHILE => while
    # LPAREN => (
    # expression => p[3] => 1 < 2
    # RPAREN => )
    # LBRACE => {
    # block => p[6] => [1 + 1, 2 + 2] => Code block
    # RBRACE => }
    p[0] = ("while", p[3], p[6])


def p_if_statement(p):
    """
    if_expression : IF LPAREN expression RPAREN LBRACE block RBRACE
    | IF LPAREN expression RPAREN LBRACE block RBRACE ELSE LBRACE block RBRACE
    """
    # IF => if
    # LPAREN => (
    # expression => p[3] => 1 < 2
    # RPAREN => )
    # LBRACE => {
    # block => p[6] => [1 + 1, 2 + 2] => Code block
    # RBRACE => }
    # ---
    # ELSE => else
    # LBRACE => {
    # block => p[10] => [1 + 1, 2 + 2] => Code block
    # RBRACE => }
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('if', p[3], p[6], p[10])


def p_function_declaration(p):
    """
    function_declaration : FUN NAME LPAREN function_parameters RPAREN LBRACE block RBRACE
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


def p_printm_message(p):
    """
    function_print : PRINTM LPAREN string RPAREN
    """
    p[0] = ("printm", p[3][1])


def p_plot(p):
    """
    function_plot : PLOT LPAREN expression COMMA NAME RPAREN
    """
    p[0] = ("plot", p[3], p[5])


def p_plot_hist(p):
    """
    function_plot : PLOTHIST LPAREN expression COMMA NAME RPAREN
    """
    p[0] = ("plotHist", p[3], p[5])


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
        # Obtiene el valor de la x si la expresión es una tupla ('var', x)
        p[0] = [run(p[1])] if type(p[1]) == tuple else [p[1]]
    else:
        # Obtiene el valor de la x si la expresión es una tupla ('var', x)
        p[0] = p[1] + [run(p[3])] if type(p[3]) == tuple else p[1] + [p[3]]


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
    # p[1] = name of the object
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
           | STRING
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
               | NAME LPAREN expression RPAREN
               | NAME DOT NAME
    """
    # Receives a = ExpoRand(5); or a = ExpoRand;
    if p[1] in list_distributions:
        p[0] = ('randList', p[1], p[3]) if len(p) > 4 else ('rand', p[1])
    else:
        p[0] = ('var', p[1])


def p_set_array_position(p):
    """
    expression : NAME LBRACKET INT RBRACKET EQUALS expression
    """
    p[0] = ('set_array_position', p[1], p[3], p[6])


def p_append_to_array(p):
    """
    expression : NAME DOT APPEND LPAREN expression RPAREN
    """
    p[0] = ('append', p[1], p[5])


def p_error(p):
    """
    Output to the user that there is an error in the input as it doesn't conform to our grammar.
    p_error is another special Ply function.
    :param p: The input that doesn't conform to our grammar.
    """
    if p is not None:
        print(Fore.RED + f"Syntax error found: {p}" + Style.RESET_ALL)


def p_empty(p):
    """
    empty :
    """
    p[0] = None


parser = yacc.yacc()  # Build the parser
env = {}  # Create the environment upon which we will store and retrieve variables from.
env_rand = {}
env_history_rand = {}


# Operators logic:


def left_right(p):
    left = run(p[1])
    right = run(p[2])
    if type(left) == list:
        left = np.array(left)
    if type(right) == list:
        right = np.array(right)

    return left, right


# Probabilistic distributions:


def get_default_value(env_key, default_value, error_message=None, warning_message=None, condition=False):
    value = env.get(env_key, default_value)

    if condition:
        print(Fore.RED + f"Error: {error_message} You used {env_key} as {value}. Defaulting to {default_value}"
                         f". Replace it using {env_key}=<{type(default_value).__name__}>;" + Style.RESET_ALL)
        value = default_value
        print(Fore.YELLOW + f"Warning: The default value {value} will be used in the meantime." + Style.RESET_ALL)
    if env_key not in env and warning_message is not None:
        print(
            Fore.YELLOW + f"Warning: {warning_message} Defaulting to {value}. Replace it using "
                          f"{env_key}=<{type(value).__name__}>;" + Style.RESET_ALL)

    env[env_key] = value
    return env[env_key]


def default_seed():
    v_default = 1
    return get_default_value('SEED', v_default, warning_message=f"SEED not set.")


def default_success():
    v_default = 0.5
    v_success = env.get('SUCCESS', 0.5)
    return get_default_value('SUCCESS', v_default, "SUCCESS must be between 0 and 1.",
                             f"SUCCESS not set. Must be a value between 0 and 1.",
                             condition=(v_success < 0 or v_success > 1))


def default_mu():
    v_default = 5
    return get_default_value('MU', v_default, warning_message=f"MU not set.")


def default_sigma():
    v_default = 1
    return get_default_value('SIGMA', v_default, warning_message=f"SIGMA not set.")


def default_lambda():
    v_default = 80
    return get_default_value('LAMBDA', v_default, warning_message=f"LAMBDA not set.")


def default_lim_sup():
    v_default = 100
    v_lim_sup = env.get('LIM_SUP', 100)
    v_lim_inf = env.get('LIM_INF', 0)
    return get_default_value('LIM_SUP', v_default, "LIM_INF must be smaller than LIM_SUP.", f"LIM_SUP not set.",
                             condition=(v_lim_inf > v_lim_sup))


def default_lim_inf():
    v_default = 0
    v_lim_sup = env.get('LIM_SUP', 100)
    v_lim_inf = env.get('LIM_INF', 0)
    return get_default_value('LIM_INF', v_default, "LIM_INF must be smaller than LIM_SUP.", f"LIM_INF not set.",
                             condition=(v_lim_inf > v_lim_sup))


def rand__rand_list(p):
    seed = default_seed()
    if len(p) == 2: p += (None,)  # To use the distribution functions that take 3 parameters.

    if p[1] in list_distributions:
        distribution_type = 'single' if p[0] == 'rand' else 'list'
        distribution_func, distribution_params = list_distributions[p[1]][distribution_type]()
        return distribution_func(seed, *distribution_params, p[2])
    else:
        print(Fore.RED + 'Distribution not found: ' + p[1] + Fore.RESET)
        print(Fore.YELLOW + f'Available distributions: {list(list_distributions.keys())}' + Fore.RESET)


list_distributions = {
    'ExpoRand': {
        'list': lambda: (lcg_rand.exponential_distribution_list, [default_lambda()]),
        'single': lambda: (lcg_rand.exponential_distribution, [default_lambda()]),
    },
    'GeoRand': {
        'list': lambda: (lcg_rand.geometric_distribution_list, [default_success()]),
        'single': lambda: (lcg_rand.geometric_distribution, [default_success()]),
    },
    'NormalRand': {
        'list': lambda: (lcg_rand.normal_distribution_list, [default_mu(), default_sigma()]),
        'single': lambda: (lcg_rand.normal_distribution, [default_mu(), default_sigma()]),
    },
    'PoissonRand': {
        'list': lambda: (lcg_rand.poisson_distribution_list, [default_lambda()]),
        'single': lambda: (lcg_rand.poisson_distribution, [default_lambda()]),
    },
    'UniformRand': {
        'list': lambda: (lcg_rand.uniform_distribution_list, [default_lim_inf(), default_lim_sup()]),
        'single': lambda: (lcg_rand.uniform_distribution, [default_lim_inf(), default_lim_sup()]),
    },
}


# Analysis tree:


def run(p):
    """
    Analysis tree:
    The run function is our recursive function that 'walks' the tree generated by our parser.
    :param p: The tree generated by our parser.
    :return: The result of the tree.
    """
    global env, env_rand, env_history_rand
    if type(p) == tuple:
        if p[0] == '+':  # LEFT + RIGHT
            left, right = left_right(p)
            return left + right
        elif p[0] == '-':  # LEFT - RIGHT
            left, right = left_right(p)
            return left - right
        elif p[0] == '*':  # LEFT * RIGHT
            left, right = left_right(p)
            return left * right
        elif p[0] == '/':  # LEFT / RIGHT
            left, right = left_right(p)
            return left / right
        elif p[0] == 'sin':  # sin(FLOAT)
            return np.sin(run(p[1]))
        elif p[0] == 'cos':  # cos(FLOAT)
            return np.cos(run(p[1]))
        elif p[0] == 'tan':  # tan(FLOAT)
            return np.tan(run(p[1]))
        elif p[0] == 'sqrt':  # sqrt(FLOAT)
            return np.sqrt(run(p[1]))
        elif p[0] == 'arcsin':  # arcsin(FLOAT)
            return np.arcsin(run(p[1]))
        elif p[0] == 'arccos':  # arccos(FLOAT)
            return np.arccos(run(p[1]))
        elif p[0] == 'arctan':  # arctan(FLOAT)
            return np.arctan(run(p[1]))
        elif p[0] == 'abs':  # abs(FLOAT)
            return np.abs(run(p[1]))
        elif p[0] == 'floor':  # floor(FLOAT)
            return np.floor(run(p[1]))
        elif p[0] == 'round':  # round(FLOAT)
            return np.round(run(p[1]))
        elif p[0] == 'ceil':  # ceil(FLOAT)
            return np.ceil(run(p[1]))
        elif p[0] == '^':  # LEFT ^ RIGHT
            return run(p[1]) ** run(p[2])
        elif p[0] == '>=':  # LEFT >= RIGHT
            return run(p[1]) >= run(p[2])
        elif p[0] == '<=':  # LEFT <= RIGHT
            return run(p[1]) <= run(p[2])
        elif p[0] == '>':  # LEFT > RIGHT
            return run(p[1]) > run(p[2])
        elif p[0] == '<':  # LEFT < RIGHT
            return run(p[1]) < run(p[2])
        elif p[0] == '==':  # LEFT == RIGHT
            return run(p[1]) == run(p[2])
        elif p[0] == 'and':  # LEFT and RIGHT
            return run(p[1]) and run(p[2])
        elif p[0] == 'or':  # LEFT or RIGHT
            return run(p[1]) or run(p[2])
        elif p[0] == '=':  # VARNAME = EXPR;
            # Multiple lists are used to store the values of the variables and the functions as data types, historical
            # data and the current values.
            env[p[1]] = run(p[2])
            env_rand[p[1]] = p[2]
            env_history_rand.setdefault(p[1], [])  # if p[1] not in env_history_rand, set it to []
        elif p[0] == 'rand':  # VARNAME = DISTRIBUTIONRand;
            return rand__rand_list(p)
        elif p[0] == 'randList':  # VARNAME = DISTRIBUTIONRand();
            return rand__rand_list(p)
        elif p[0] == 'values':  # VARNAME = VARNAME.values();
            return env_history_rand[p[1]]
        elif p[0] == 'print':  # print(VARNAME);
            print(run(p[1]))
        elif p[0] == 'array_get':  # VARNAME[INDEX];
            return env[p[1]][run(p[2])]
        elif p[0] == 'set_array_position':  # VARNAME[INDEX] = EXPR;
            if type(env[p[1]]) == list:
                if len(env[p[1]]) <= run(p[2]):
                    print(Fore.RED + f"Error: index {run(p[2])} out of range in'{p[1]}' " + Style.RESET_ALL)
                    return None
                env[p[1]][run(p[2])] = run(p[3])
            else:
                print(Fore.RED + f"Error: '{p[1]}' is not a list" + Style.RESET_ALL)
        elif p[0] == 'append':  # VARNAME.append(EXPR);
            env[p[1]].append(run(p[2]))
        elif p[0] == 'len':  # len(VARNAME);
            return int(len(run(p[1])))
        elif p[0] == 'model':  # VARNAME = model(VARNAME, VARNAME, VARNAME, VARNAME);
            return alg.Model(run(p[1]), run(p[2]), run(p[3]), run(p[4]))
        elif p[0] == 'operationNum':  # VARNAME = VARNAME.operationNum(NUMBER);
            # p[0] = name of the function
            # p[1] = name of the object
            # p[2] = parameters
            if p[1] not in env:
                print(Fore.RED + f'Error: object {p[1]} is not defined' + Style.RESET_ALL)
                return
            return env[p[1]].operationNum(run(p[2][0]), run(p[2][1]))
        elif p[0] == 'operationSet':  # VARNAME = VARNAME.operationSet(NUMBER, NUMBER);
            if p[1] not in env:
                print(Fore.RED + f'Error: object {p[1]} is not defined' + Style.RESET_ALL)
                return
            return env[p[1]].operationSet(run(p[2][0]), run(p[2][1]))
        elif p[0] == 'toStreakModel':  # VARNAME = VARNAME.toStreakModel();
            if p[1] not in env:
                print(Fore.RED + f'Error: object {p[1]} is not defined' + Style.RESET_ALL)
                return
            return env[p[1]].toSteakModel()
        elif p[0] == 'steakOperationSum':
            if p[1] not in env:
                print(Fore.RED + f'Error: object {p[1]} is not defined' + Style.RESET_ALL)
                return
            return env[p[1]].steakOperationSum(run(p[2][0]), run(p[2][1]), run(p[2][2]))
        elif p[0] == 'SteakOperationAvrg':
            if p[1] not in env:
                print(Fore.RED + f'Error: object {p[1]} is not defined' + Style.RESET_ALL)
                return
            return env[p[1]].SteakOperationAvrg(run(p[2][0]), run(p[2][1]), run(p[2][2]))
        elif p[0] == 'chain':
            return alg.Chain(p[1])

        elif p[0] == 'numberOfSteaks':  # VARNAME = VARNAME.numberOfSteaks();
            if p[1] not in env:
                print(Fore.RED + f'Error: object {p[1]} is not defined' + Style.RESET_ALL)
                return
            return env[p[1]].numberOfSteaks()

        elif p[0] == 'numberOfSteaksUntilIndex':  # VARNAME = VARNAME.numberOfSteaksUntilIndex(NUMBER);
            if p[1] not in env:
                print(Fore.RED + f'Error: object {p[1]} is not defined' + Style.RESET_ALL)
                return
            return env[p[1]].numberOfSteaksUntilIndex(p[2][0])
        elif p[0] == 'printm':  # printm(VARNAME/STRING);
            print(p[1])
        elif p[0] == 'plot':  # plot(VARNAME, GRAPH_NAME);
            if type(p[1]) == "str" and p[1] not in env:
                print(Fore.RED + f'Error: object {p[1]} is not defined' + Style.RESET_ALL)
                return
            alg.showPlot(run(p[1]), run(p[2]))
        elif p[0] == 'plotHist':  # plotHist(VARNAME, GRAPH_NAME);
            if type(p[1]) == "str" and p[1] not in env:
                print(Fore.RED + f'Error: object {p[1]} is not defined' + Style.RESET_ALL)
                return
            alg.show_plot_histogram(run(p[1]), run(p[2]))
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
                print(Fore.YELLOW + "Warning: Function not found: ", name + Style.RESET_ALL)
                return None

            function_values = env[name]
            # function_values[1] are the arguments of the function
            # function_values[2] are the statements of the function
            if function_values[0] != "function":
                print(Fore.YELLOW + "Warning: Not a function:", name + Style.RESET_ALL)
                return None
            if len(function_values[1]) != len(args):
                print(Fore.YELLOW + f"Warning: Argument count mismatch, the function requires "
                                    f"{len(function_values[1])} arguments but you supplied {len(args)}"
                                    f"" + Style.RESET_ALL)
                return None
            # Add the arguments to the new environment
            for i in range(len(args)):
                env[function_values[1][i]] = env[args[i]]
            run(function_values[2])
        elif p[0] == 'if':  # if (CONDITION) { STATEMENTS } else { STATEMENTS }
            if run(p[1]):
                return run(p[2])
            else:
                if len(p) > 3:
                    return run(p[3])
        elif p[0] == 'block':  # { STATEMENTS }
            for x in p[1]:
                run(x)
        elif p[0] == 'while':  # while (CONDITION) {
            while run(p[1]):
                run(p[2])
        elif p[0] == 'var':  # VARNAME = EXPRESSION;
            if p[1] not in env:
                print(Fore.YELLOW + f"Warning: Undeclared variable found! {p[1]}" + Style.RESET_ALL)
            else:
                if type(env_rand[p[1]]) == tuple and (env_rand[p[1]][0] == 'rand' or env_rand[p[1]][0] == 'randList'):
                    get_rand_value = run(env_rand[p[1]])
                    env[p[1]] = get_rand_value
                    env_history_rand[p[1]].append(get_rand_value)
                return env[p[1]]
    else:
        return p


# Execution and signal handler


def exe(tokenize=False, file_name=None):
    """
    With the user input 'tokenize' and 'file_name' it will execute the code following:
    If the user enters a file name, it will execute the code in the file
    If the user not, it will execute the code through the terminal
    :param tokenize: boolean
    :param file_name: string
    """
    if file_name:
        execution.execute_file(file_name=file_name, tokenize=tokenize, parser=parser, lexer=lexer)  # execute from file
    else:
        while True:
            try:
                s = input('PScript >> ')
            except EOFError:
                break
            execution.execute_code(code=s, tokenize=tokenize, parser=parser, lexer=lexer)  # execute code in terminal


def signal_handler(signal, frame):
    print(Fore.YELLOW + '\n\nYou pressed Ctrl+C!' + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + 'Exiting from PScript...' + Style.RESET_ALL)
    sys.exit(0)


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
    signal.signal(signal.SIGINT, signal_handler)
    main()
