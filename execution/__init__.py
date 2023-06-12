def execute_code(code, tokenize=False, is_a_file=False, parser=None, lexer=None):
    """
    With the user input 'code' it will execute the code line by line on console
    When it finds a block of code it will execute it as a block
    :param code: the code to execute
    :param tokenize: if True it will tokenize the code
    :param is_a_file: if True it won't show the prompt to introduce code in brackets
    :param parser: the parser to use
    :param lexer: the lexer to use
    """
    open_braces = 0
    close_braces = 0
    in_block = False
    block_code = ""

    lines = code.splitlines()
    num_lines = len(lines)
    i = 0

    while i < num_lines:
        line = lines[i]

        if '{' in line:
            open_braces += line.count('{')
            close_braces += line.count('}')

            if not in_block:
                in_block = True
                block_code = ""

        if in_block:
            block_code += line.strip()

        if '}' in line:
            close_braces += line.count('}')
            open_braces -= line.count('{')

            if open_braces == close_braces and in_block:
                if not tokenize:
                    parser.parse(block_code)
                else:
                    lexer.input(block_code)
                    while True:
                        tok = lexer.token()
                        if not tok:
                            break
                        print(tok)

                in_block = False
                block_code = ""

        elif open_braces > 0 and in_block:
            input_lines = [line]  # Initialize with the current line
            i += 1
            while i < num_lines:
                input_lines.append(lines[i])
                block_code += lines[i].strip()
                if '}' in lines[i]:
                    close_braces += lines[i].count('}')
                    open_braces -= lines[i].count('{')
                    if open_braces == close_braces:
                        break
                i += 1

            # Prompt for input until all braces are closed
            if not is_a_file:
                while open_braces != close_braces:
                    try:
                        input_line = input("PScript >>... ")
                        input_lines.append(input_line)
                        block_code += input_line.strip()
                        open_braces += input_line.count('{')
                        close_braces += input_line.count('}')
                    except KeyboardInterrupt:
                        break

            # Execute the block of code
            if not tokenize:
                parser.parse(block_code)
            else:
                lexer.input(block_code)
                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    print(tok)

        elif open_braces == 0 and not in_block:
            if not tokenize:
                parser.parse(line)
            else:
                lexer.input(line)
                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    print(tok)

        i += 1


def execute_file(file_name, tokenize=False, parser=None, lexer=None):
    """
    With the user input 'file_name' it will execute the code in the file
    :param file_name: the name of the file
    :param tokenize: if True it will tokenize the code
    :param parser: the parser to use
    :param lexer: the lexer to use
    """
    if file_name:
        with open(file_name) as f:
            code = f.read()
            execute_code(code, tokenize=tokenize, is_a_file=True, parser=parser, lexer=lexer)
