import sys
import re


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

    def read_cache(self, location):
        return self.bus.read_cache(location)

    def evaluate_parameter(self, operand):
        # read register
        for reg in self.GR.reg_list:
            if reg in operand:
                operand = operand.replace(reg, str(self.GR.read(reg)))
        # access memory
        if '[' in operand:
            operand = operand.replace('[', '').replace(']', '')
            operand = self.read_cache(operand)
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

    def control_circuit(self):
        data_transfer_ins = ['MOV', 'PUSH', 'POP', 'IN', 'OUT']
        arithmetic_ins = ['ADD', 'SUB', 'INC', 'DEC', 'MUL', 'IMUL', 'DIV', 'IDIV', 'CMP']
        bit_manipulation_ins = ['NOT', 'AND', 'OR', 'XOR', 'TEST', 'SHL', 'SAL', 'SHR', 'SAR']
        program_transfer_ins = ['RET', 'JMP', 'INT']
        string_ins = []
        
        if self.opcode in data_transfer_ins:
            self.data_transfer()
        elif self.opcode in arithmetic_ins:
            self.alu()
        elif self.opcode in bit_manipulation_ins:
            self.alu_bit()
        elif self.opcode in program_transfer_ins:
            self.program_transfer()
        elif self.opcode in string_ins:
            self.string_operation()
        else:
            sys.exit("operation code not support")

    def data_transfer(self):
        if self.opcode == 'MOV':
            result = self.eo[1]
            if self.oprands[0] in self.GR.reg_list:
                self.GR.write(self.oprands[0], result)
            elif '[' in self.oprands[0]:
                target_location = self.oprands[0].replace('[', '').replace(']', '')
                cpu.cache.write(target_location, result)
        else:
            pass        

    def alu(self):
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


    def alu_bit(self):
        pass

    def program_transfer(self):
        if self.opcode == 'JMP':
            self.bus.IP = self.eo[0]
        else:
            pass

    def string_operation(self):
        pass