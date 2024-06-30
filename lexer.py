# Lexer (lexical analysis)

from tokens import reserved_tokens
import re

## Capture tokens that fit token definitions in token.py via regex
## String literals and comments are special cases
## Newlines aren't captured
def lex(text):
    # Store tokens (type, pattern) pair here
    tokens = []

    # Track line number for debugging
    line_no = 1
    
    # When obtw is true, the lexer will NOT add tokens
    obtw = False

    imported_tokens = list(reserved_tokens.items())

    # Go thru each line in the file
    for line in text:
        line = line.lstrip()


        # Flag for checking if a match is found
        match_found = False

        while line:
            i = 0
            while i < len(imported_tokens):
                type, pattern = imported_tokens[i]
                match = re.match(pattern, line)      
                if match:
                    i = 0  # Reset search when match is found within the same line
                    match_found = True
                    ## SKIP COMMENTS
                    # Lines that follow an OBTW should be commented out
                    # TLDR - end multi-line comment
                    if type == "Multi-line Comment End":
                        obtw = False
                        line = ""
                        break
                    elif obtw:
                        line = ""
                        break
                    # BTW - Single-line comments
                    elif type == "Single-line Comment Delimiter":
                        line = ""
                        break
                    # OBTW - start of multi-line comment
                    elif obtw == False and type == "Multi-line Comment Delimiter":
                        obtw = True
                        line = ""
                        break
                    ## Yarn - strings should be wrapped with a ""
                    elif type == "String Literal":
                        captured_value = match.group(0)
                        tokens.append(("String Delimiter", '"', line_no))
                        tokens.append((type, captured_value, line_no))
                        tokens.append(("String Delimiter", '"', line_no))
                    else:
                        captured_value = match.group(0)
                        tokens.append((type, captured_value, line_no))
                    line = line[len(captured_value):].lstrip()
                i += 1

            # Unrecognized token (no match) will return an error
            if not match_found:
                return {"tokens": None, "error": f"Lexer Error: Unrecognized lexeme at line {line_no}"}
            # Reset flag
            match_found = False

        # Add a new line token per new line
        tokens.append(("Newline", "\n", line_no))

        # Update line tracker
        line_no += 1
    
    return {"tokens": tokens, "error": None}