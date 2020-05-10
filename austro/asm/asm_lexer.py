
from ply import lex

instructions = (
        'ADD', 'AND', 'CMP', 'DEC', 'DIV', 'HALT', 'ICMP', 'IDIV', 'IMOD',
        'IMUL', 'INC', 'JE', 'JGE', 'JGT', 'JLE', 'JLT', 'JMP', 'JN', 'JNE',
        'JNZ', 'JP', 'JT', 'JV', 'JZ', 'MOD', 'MOV', 'MUL', 'NOP', 'NOT', 'OR',
        'SHL', 'SHR', 'SUB', 'XOR', 'SEG'
    )
tokens = ("LABEL", "OPCODE", "NAME", "REFERENCE", "NUMBER", "COMMA", "COMMENT")

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'
t_COMMA = ','

def get_base(t_name):
    base = None
    if t_name.startswith("0b"):
        base = 2
    elif t_name.startswith("0x"):
        base = 16
    elif t_name.startswith("0"):
        base = 8
    else:
        base = 10
    return base


number = r'(0b[01]+|0[0-7]+|0o[0-7]+|0x[0-9a-fA-F]+|-?\d+)'
reference = r'\[\s*' + number + r'\s*\]'

def t_newline(t):
    r'\r\n|\n'  # no support to only \r
    t.lexer.lineno += 1

def t_LABEL(t):
    r'[a-zA-Z_.][a-zA-Z0-9_.]*\s*:'
    t.value = t.value.rstrip(' \t:')
    return t

@lex.TOKEN(reference)
def t_REFERENCE(t):
    t.value = t.value.strip(' \t[]')
    t.value = int(t.value, get_base(t.value))
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in instructions:
        t.type = "OPCODE"
    return t

@lex.TOKEN(number)
def t_NUMBER(t):
    t.value = int(t.value, get_base(t.value))
    return t

def t_error(t):
    raise LexerException("Scanning error. Illegal character '%s' at line %d" % \
            (t.value[0], t.lineno))


def get_lexer():
    return lex.lex()


class LexerException(Exception):
    pass


if __name__ == "__main__":
    get_lexer()
    lex.runmain()
