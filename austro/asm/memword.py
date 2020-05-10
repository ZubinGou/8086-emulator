
import ctypes

from austro.abstractdata import AbstractData


class Word(AbstractData, ctypes.Structure):
    '''Represent the memory word

    Word objects can act as instruction or data words of 16 bits
    '''

    _fields_ = [('_opcode', ctypes.c_ubyte, 5),
                ('_flags', ctypes.c_ubyte, 3),
                ('_operand', ctypes.c_ubyte, 8),
                ('_value', ctypes.c_uint16)]
    _bits = 16

    def __init__(self, opcode=0, flags=0, operand=0, lineno=0, value=None,
            is_instruction=False):
        # Flag to know if this word should act as a instruction
        self._instruction = is_instruction
        # Set an associated assembly code line number (for instructions)
        self.lineno = lineno

        if value is not None:
            self.value = value
        else:
            # If marked as instruction, set args separately
            if is_instruction:
                ctypes.Structure.__init__(self, opcode, flags, operand)
            # In a data word the 'opcode' arg act as whole value
            else:
                self.value = opcode

    @property
    def value(self):
        if self.is_instruction:
            return (self.opcode << 3 | self.flags) << 8 | self.operand
        else:
            return self._value
    @value.setter
    def value(self, value):
        if self.is_instruction:
            self.opcode = value >> 11
            self.flags = value >> 8
            self.operand = value
        else:
            self._value = value

    @property
    def opcode(self):
        assert self.is_instruction, "Word is not a instruction"
        return self._opcode
    @opcode.setter
    def opcode(self, value):
        assert self.is_instruction, "Word is not a instruction"
        self._opcode = value

    @property
    def flags(self):
        assert self.is_instruction, "Word is not a instruction"
        return self._flags
    @flags.setter
    def flags(self, value):
        assert self.is_instruction, "Word is not a instruction"
        self._flags = value

    @property
    def operand(self):
        assert self.is_instruction, "Word is not a instruction"
        return self._operand
    @operand.setter
    def operand(self, value):
        assert self.is_instruction, "Word is not a instruction"
        self._operand = value

    @property
    def is_instruction(self):
        return self._instruction
    @is_instruction.setter
    def is_instruction(self, switch):
        if switch:
            if not self._instruction:
                self._instruction = True
                self.value = self._value
        else:
            if self._instruction:
                value = self.value
                self._instruction = False
                self.value = value

    @property
    def is_data(self):
        return not self._instruction
    @is_data.setter
    def is_data(self, switch):
        self.is_instruction = not switch

    def __eq__(self, o):
        return self.value == o.value

    def __repr__(self):
        if self.is_instruction:
            return 'Word(%d, %d, %d, lineno=%d)' % (self.opcode,
                                        self.flags, self.operand, self.lineno)
        else:
            return 'Word(%d)' % (self._value)
