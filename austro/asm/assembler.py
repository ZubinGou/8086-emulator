
from austro.asm.asm_lexer import get_lexer
from austro.asm.memword import Word


OPCODES = {
        # Control Unit instructions
        'NOP': 0b00000, 'HALT': 0b00001, 'MOV': 0b00010,  'JZ':  0b00011,
        'JE':  0b00011, 'JNZ':  0b00100, 'JNE': 0b00100,  'JN':  0b00101,
        'JLT': 0b00101, 'JP':   0b00110, 'JGT': 0b00110,  'JGE': 0b00111,
        'JLE': 0b01000, 'JV':   0b01001, 'JT':  0b01010,  'JMP': 0b01011,
        'SEG': 0b01110,
        # Shift Unit instructions
        'SHR': 0b01100, 'SHL':  0b01101,
        # ALU instructions
        'ADD': 0b10000,  'INC': 0b10001, 'DEC': 0b10010, 'SUB':  0b10011,
        'MUL': 0b10100, 'IMUL': 0b10100, 'OR':  0b10101, 'AND':  0b10110,
        'NOT': 0b10111, 'XOR':  0b11000, 'DIV': 0b11001, 'IDIV': 0b11001,
        'MOD': 0b11010, 'IMOD': 0b11010, 'CMP': 0b11011, 'ICMP': 0b11011,
    }

REGISTERS = {
        'AL': 0b0000, 'AH': 0b0001, 'BL': 0b0010, 'BH': 0b0011,
        'CL': 0b0100, 'CH': 0b0101, 'DL': 0b0110, 'DH': 0b0111,
        'AX': 0b1000, 'BX': 0b1001, 'CX': 0b1010, 'DX': 0b1011,
        'SP': 0b1100, 'BP': 0b1101, 'SI': 0b1110, 'DI': 0b1111,
    }


def memory_words(opcode, op1=None, op2=None):
    """Construct memory words using Word objects

    The output of this function is a tuple of one or two elements.

    If compounded of one element, this element is a Word object marked as
    instruction word.

    If compounded of two elements, then
    - first is a Word object marked as instruction and
    - second is another Word object marked as data.
    """
    opname = opcode.value.upper()
    try:
        instr_word = Word(OPCODES[opname], lineno=opcode.lineno, is_instruction=True)
    except KeyError:
        raise AssembleException("Invalid instruction '%s'" % opname,
                opcode.lineno)

    # zero-operand instructions
    if op1 is None:
        if opname in ('NOP', 'HALT'):
            return (instr_word,)

    # 1-operand instructions
    elif op2 is None:
        jumps = ('JE', 'JGE', 'JGT', 'JLE', 'JLT', 'JMP',
                 'JN', 'JNE', 'JNZ', 'JP', 'JT', 'JV', 'JZ',)
        others = ('DEC', 'INC', 'NOT', 'SEG')
        # Jump instructions
        if opname in jumps:
            if op1.type == 'NAME':
                try:
                    instr_word.operand = REGISTERS[op1.value.upper()] << 4
                    instr_word.flags = 0
                except KeyError:
                    raise AssembleException("Error: bad register name '%s'" %
                            op1.value, op1.lineno)

                return (instr_word,)
            elif op1.type == 'REFERENCE':
                instr_word.operand = op1.value
                instr_word.flags = 1
                return (instr_word,)
            elif op1.type == 'NUMBER':
                instr_word.operand = op1.value
                instr_word.flags = 2
                return (instr_word,)

        # INC, DEC, NOT and SEG instructions
        elif opname in others:
            if op1.type == 'NAME':
                try:
                    instr_word.operand = REGISTERS[op1.value.upper()] << 4
                    instr_word.flags = 0
                except KeyError:
                    raise AssembleException("Error: bad register name '%s'" %
                            op1.value, op1.lineno)

                return (instr_word,)
            elif op1.type == 'REFERENCE':
                instr_word.operand = op1.value
                instr_word.flags = 1
                return (instr_word,)

    # 2-operand instructions
    else:
        shifts = ('SHR', 'SHL',)
        others = ('MOV', 'CMP', 'ICMP', 'DIV', 'IDIV', 'MOD', 'IMOD',
                  'MUL', 'IMUL', 'AND', 'OR', 'XOR', 'ADD', 'SUB',)
        # Shift instructions
        if opname in shifts:
            if op2.type == 'NUMBER':
                if op1.type == 'NAME':
                    try:
                        instr_word.operand = REGISTERS[op1.value.upper()] << 4
                        instr_word.flags = 0
                    except KeyError:
                        raise AssembleException("Error: bad register name '%s'"
                                % op1.value, op1.lineno)

                    return (instr_word, Word(op2.value))
                elif op1.type == 'REFERENCE':
                    instr_word.operand = op1.value
                    instr_word.flags = 1
                    return (instr_word, Word(op2.value))
                else:
                    raise AssembleException("Error: invalid operands",
                            op1.lineno)
        # All other instructions
        elif opname in others:
            if opname in ('ICMP', 'IDIV', 'IMOD', 'IMUL',):
                instr_word.flags = 0b100  # signed instructions

            if op1.type == 'NAME' and op2.type == 'NAME':
                try:
                    instr_word.operand = REGISTERS[op1.value.upper()] << 4
                    instr_word.operand |= REGISTERS[op2.value.upper()]
                    # flag x00 - no needs to set
                except KeyError as e:
                    bad_reg = op1 if e.args == op1.value.upper() else op2
                    raise AssembleException("Error: bad register name '%s'" %
                            bad_reg.value, bad_reg.lineno)

                return (instr_word,)
            elif op1.type == 'NAME' and op2.type == 'REFERENCE':
                try:
                    instr_word.operand = REGISTERS[op1.value.upper()] << 4
                    instr_word.flags |= 0b001  # flag x01
                except KeyError:
                    raise AssembleException("Error: bad register name '%s'" %
                            op1.value, op1.lineno)

                return (instr_word, Word(op2.value))
            elif op1.type == 'NAME' and op2.type == 'NUMBER':
                try:
                    instr_word.operand = REGISTERS[op1.value.upper()] << 4
                    instr_word.flags |= 0b010  # flag x10
                except KeyError:
                    raise AssembleException("Error: bad register name '%s'" %
                            op1.value, op1.lineno)

                return (instr_word, Word(op2.value))
            elif op1.type == 'REFERENCE' and op2.type == 'NAME':
                try:
                    instr_word.operand = REGISTERS[op2.value.upper()] << 4
                    instr_word.flags |= 0b011  # flag x11
                except KeyError:
                    raise AssembleException("Error: bad register name '%s'" %
                            op2.value, op2.lineno)

                return (instr_word, Word(op1.value))
            else:
                raise AssembleException("Error: invalid operands",
                        op1.lineno)

    return None


def assemble(code):
    """Analyzes assembly code and returns a dict of labels and memory words

    The returned dict is in the following format:

        {'labels': {
                'loop': 6,  # loop is a label and 1 the associated address
                'rept': 8,
                ...
            }
         'words': [
                Word(5, 7, 46, lineno=1),  # instruction word
                Word(2028),                # data word
                ...
            ]
        }

    As can be seen, the labels itself are another dict where the key is a
    label name and the value the following instruction associated address.

    The 'words' key is a list of Word objects representing 16-bit words,
    intended to be a kind of Austro Simulator assembler.

    The Word object (instruction) carry lineno attribute that is the associated
    line number in assembly file.
    """
    lexer = get_lexer()
    lexer.input(code)

    # Structures to store labels and memory words
    labels = {}
    words = []


    def verify_pending_labels():
        # Verify if has any label pending an address
        while pend_labels:
            lbl = pend_labels.pop()
            if lbl.value in labels:
                raise AssembleException(
                        "Error: symbol '%s' is already defined." % lbl.value,
                        lbl.lineno)
            # Point the label to the next word pending attribution
            position = len(words)
            labels[lbl.value] = position
            # Verify if has any jump instruction missing this label
            mlbls = miss_labels.get(lbl.value)
            if mlbls:
                for mlb in mlbls:
                    mlb.operand = position
                del miss_labels[lbl.value]

    opcode = None
    pend_labels = []
    miss_labels = {}
    tok = lexer.token()
    while tok:
        if tok.type == 'LABEL':
            pend_labels.append(tok)

        elif tok.type == 'OPCODE':
            verify_pending_labels()

            # Store opcode
            opcode = tok

            # Get first operator if available
            tok = lexer.token()
            if not tok or tok.lineno != opcode.lineno:
                words.extend(memory_words(opcode))  # non-arg opcode
                continue
            op1 = tok

            # Comma
            tok = lexer.token()
            if not tok or tok.lineno != opcode.lineno:
                # If instruction is a jump, replace labels by it address
                jumps = ('JE', 'JGE', 'JGT', 'JLE', 'JLT', 'JMP',
                         'JN', 'JNE', 'JNZ', 'JP', 'JT', 'JV', 'JZ',)
                no_label = False
                lbl_name = op1.value
                if op1.type == 'NAME' and opcode.value.upper() in jumps:
                    if op1.value.upper() not in REGISTERS:
                        op1.type = 'NUMBER'
                        if op1.value not in labels:
                            no_label = True
                            op1.value = 0
                        else:
                            op1.value = labels[op1.value]

                words.extend(memory_words(opcode, op1))  # 1-arg opcode
                if no_label:
                    if lbl_name not in miss_labels:
                        miss_labels[lbl_name] = []
                    miss_labels[lbl_name].append(words[-1])
                continue
            if tok.type != 'COMMA':
                raise AssembleException("Invalid token '%s'" % tok.value,
                        tok.lineno)

            # Get second operator if available
            tok = lexer.token()
            if not tok or tok.lineno != opcode.lineno:
                raise AssembleException("Invalid syntax", opcode.lineno)
            op2 = tok

            words.extend(memory_words(opcode, op1, op2))  # 2-arg opcode

        # At start of line, only labels and opcodes are allowed
        else:
            raise AssembleException("Invalid token '%s'" % tok.value,
                    tok.lineno)

        tok = lexer.token()

    # Add any pending label to labels dict
    verify_pending_labels()

    # Interrupt assembling if has any jump missing label
    for mlb in list(miss_labels.items()):
        raise AssembleException("Invalid label '%s'" % mlb[0],
                mlb[1][0].lineno)

    return {'labels': labels, 'words': words}


class AssembleException(Exception):
    def __init__(self, message, lineno):
        super(AssembleException, self).__init__(message +
                " at line %d" % lineno)


def main():
    import sys
    try:
        filename = sys.argv[1]
        f = open(filename)
        data = f.read()
        f.close()
    except IndexError:
        data = sys.stdin.read()

    from pprint import pprint
    pprint(assemble(data))


if __name__ == "__main__":
    main()
