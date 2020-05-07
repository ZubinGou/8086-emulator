import sys
import re
from instructions import *

class execution_unit(object):

    def __init__(self, register_file, BIU):
        self.IR = []                 # 指令寄存器
        self.opcode = ''             # 操作码
        self.oprands = []            # 操作数
        self.eo = [0] * 5            # Evaluated operands
        self.GR = register_file.GR   # AX BX CX DX
        self.FR = register_file.FR   # Flag Register
        self.SP = register_file.SP
        self.BP = register_file.BP
        self.SI = register_file.SI
        self.DI = register_file.DI

        self.bus = BIU # 内部总线连接BIU

    def run(self):
        self.IR = self.bus.instruction_queue.get()
        self.opcode = self.IR[0]
        if len(self.IR) > 1:
            self.oprands = self.IR[1:]
        self.instruction_decoder()
        self.evaluate_all_oprands()
        self.control_circuit()

    def evaluate_parameter(self, operand):
        # read register
        for reg in self.GR.list:
            if reg in operand:
                operand = operand.replace(reg, str(self.GR.read(reg)))
        # access memory
        if '[' in operand:
            operand = operand.replace('[', '').replace(']', '')
            operand = self.bus.read_cache(operand)
        return int(operand)

    def evaluate_all_oprands(self):
        for i in range(len(self.oprands)):
            self.eo[i] = self.evaluate_parameter(self.oprands[i])

    def instruction_decoder(self):
        # 数制转换
        ins = self.oprands
        if len(ins) < 1:
            return
        for i in range(len(ins)):
            # 十六进制转换为十进制
            hex_number = re.findall(r'[0-9A-F]+H', ins[i])
            if hex_number:
                ins[i] = ins[i].replace(hex_number[0], str(int(hex_number[0].strip('H'), 16)))
            # 二进制转换为十进制
            bin_number = re.findall(r'[01]+B', ins[i])
            if bin_number:
                ins[i] = ins[i].replace(bin_number[0], str(int(bin_number[0].strip('B'), 2)))

    def address_generate(self, segment, offset):
    # address generation circuit
        return segment * 16 + offset

    def control_circuit(self):
       


        if self.opcode in data_transfer_ins:
            self.data_transfer_ins()
        elif self.opcode in arithmetic_ins:
            self.arithmetic_ins()
        elif self.opcode in logical_ins:
            self.logical_ins()
        elif self.opcode in rotate_shift_ins:
            self.rotate_shift_ins()
        elif self.opcode in transfer_control_ins:
            self.transfer_control_ins()
        elif self.opcode in string_manipulation_ins:
            self.string_manipulation_ins()
        elif self.opcode in flag_manipulation_ins:
            self.flag_manipulation_ins()
        elif self.opcode in stack_related_ins:
            self.stack_related_ins()
        elif self.opcode in input_output_ins:
            self.input_output_ins()
        elif self.opcode in miscellaneous_ins:
            self.miscellaneous_ins()
        else:
            sys.exit("operation code not support")

    def data_transfer_ins(self):
        if self.opcode == 'MOV':
            result = self.eo[1]
            if self.oprands[0] in self.GR.list:
                self.GR.write(self.oprands[0], result)
            elif '[' in self.oprands[0]:
                location = self.oprands[0].replace('[', '').replace(']', '')
                self.bus.write_cache(location, result)
        elif self.opcode == 'XCHG':
            pass
        elif self.opcode == 'LEA':
            pass
        elif self.opcode == 'LDS':
            pass
        elif self.opcode == 'LES':
            pass
        else:
            pass        

    def arithmetic_ins(self):
        if self.opcode == 'ADD':
            result = self.eo[0] + self.eo[1]
            self.GR.write(self.oprands[0], result)

        elif self.opcode == 'SUB':
            result = self.eo[0] - self.eo[1]
            self.GR.write(self.oprands[0], result)

        elif self.opcode == 'MUL': 
            result = self.eo[0] * self.GR.read_int('AX')
            self.GR.write('AX', result)

        elif self.opcode == 'DIV':
            divisor = self.eo[0]
            divident = int(self.GR.read('AX'))
            quotient = divident // divisor
            remainder = divident % divisor
            self.GR.write('AX', quotient)
            self.GR.write('DX', remainder)
        
        elif self.opcode == 'INC':
            result = self.eo[0] + 1
            self.GR.write(self.oprands[0], result)

        elif self.opcode == 'DEC':
            result = self.eo[0] - 1
            self.GR.write(self.oprands[0], result)

        else:
            sys.exit("operation code not support")

    def logical_ins(self):
        if self.opcode == 'AND':
            pass
        elif self.opcode == 'OR':
            pass
        elif self.opcode == 'XOR':
            pass
        elif self.opcode == 'NOT':
            pass
        elif self.opcode == 'NEG':
            pass
        elif self.opcode == 'CPM':
            pass
        elif self.opcode == 'TEST':
            pass
        else:
            sys.exit("operation code not support")

    def rotate_shift_ins(self):
        if self.opcode == 'RCL':
            pass
        elif self.opcode == 'RCR':
            pass
        elif self.opcode == 'ROL':
            pass
        elif self.opcode == 'ROR':
            pass
        elif self.opcode == 'SAL':
            pass
        elif self.opcode == 'SHL':
            pass
        elif self.opcode == 'SAR':
            pass
        elif self.opcode == 'SHR':
            pass
        else:
            sys.exit("operation code not support")

    def transfer_control_ins(self):
        if self.opcode == 'JMP':
            self.bus.IP = self.eo[0]
        elif self.opcode == 'JA':
            pass
        else:
            sys.exit("operation code not support")

    def string_manipulation_ins(self):
        if self.opcode == 'MOVS':
            pass
        elif self.opcode == 'CMPS':
            pass
        elif self.opcode == 'LODS':
            pass
        elif self.opcode == 'STOS':
            pass
        elif self.opcode == 'SCAS':
            pass 
        elif self.opcode == 'REP':
            pass 
        elif self.opcode == 'REPE':
            pass 
        elif self.opcode == 'REPZ':
            pass 
        elif self.opcode == 'REPNE':
            pass 
        elif self.opcode == 'REPNZ':
            pass
        else:
            sys.exit("operation code not support")

    def flag_manipulation_ins(self):
        if self.opcode == 'STC':
            pass
        elif self.opcode == 'CLC':
            pass
        elif self.opcode == 'CMC':
            pass
        elif self.opcode == 'STD':
            pass
        elif self.opcode == 'CLD':
            pass
        elif self.opcode == 'STI':
            pass
        elif self.opcode == 'CLI':
            pass
        elif self.opcode == 'LANF':
            pass
        elif self.opcode == 'SANF':
            pass
        else:
            sys.exit("operation code not support")

    def stack_related_ins(self):
        if self.opcode == 'PUSH':
            pass
        elif self.opcode == 'POP':
            pass
        elif self.opcode == 'PUSHF':
            pass
        elif self.opcode == 'POPF':
            pass
        else:
            sys.exit("operation code not support")

    def input_output_ins(self):
        if self.opcode == 'IN':
            pass
        elif self.opcode == 'OUT':
            pass
        else:
            sys.exit("operation code not support")

    def miscellaneous_ins(self):
        if self.opcode == 'NOP':
            pass
        elif self.opcode == 'INT':
            pass
        elif self.opcode == 'IRET':
            pass
        elif self.opcode == 'XLAT':
            pass
        elif self.opcode == 'HLT':
            pass
        elif self.opcode == 'ESC':
            pass
        elif self.opcode == 'INTO':
            pass
        elif self.opcode == 'LOCK':
            pass
        elif self.opcode == 'WAIT':
            pass
        else:
            sys.exit("operation code not support")