import sys
import re


class execution_unit(object):

    def __init__(self, general_register, flag_register):
        self.instruction_register = []  # 指令寄存器
        self.opcode = ''             # 操作码
        self.oprands = []            # 操作数
        self.flag_register = flag_register  # 标志寄存器
        self.general_register = general_register # 通用寄存器
        pass

    def run(self, cpu):
        self.instruction_register = cpu.bus_interface_unit.instruction_queue.get()
        self.opcode = self.instruction_register[0]
        if len(self.instruction_register) > 1:
            self.oprands = self.instruction_register [1:]
        self.instruction_decoder(cpu)
        self.control_circuit(cpu)

    def instruction_decoder(self, cpu):
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

    def evaluate_parameter(self, operand, cpu):
        # [AX] [202] AX -> 202
        # operand is string
        for reg in self.general_register.reg_list:
            if reg in operand:
                operand = operand.replace(reg, str(self.general_register.read(reg)))

        if '[' in operand:
            operand = operand.replace('[', '').replace(']', '')
            operand = cpu.bus_interface_unit.cache_memory.read_cache_location(operand)
        return int(operand)

    def control_circuit(self, cpu):
        data_transfer_ins = ['MOV', 'PUSH', 'POP', 'IN', 'OUT']
        arithmetic_ins = ['ADD', 'SUB', 'INC', 'DEC', 'MUL', 'IMUL', 'DIV', 'IDIV', 'CMP']
        bit_manipulation_ins = ['NOT', 'AND', 'OR', 'XOR', 'TEST', 'SHL', 'SAL', 'SHR', 'SAR']
        program_transfer_ins = ['RET', 'JMP', 'INT']
        string_ins = []
        
        if self.opcode in data_transfer_ins:
            self.data_transfer(cpu)
        elif self.opcode in arithmetic_ins:
            self.alu(cpu)
        elif self.opcode in bit_manipulation_ins:
            self.alu_bit(cpu)
        elif self.opcode in program_transfer_ins:
            self.program_transfer(cpu)
        elif self.opcode in string_ins:
            self.string_operation(cpu)
        else:
            sys.exit("operation code not support")

    def data_transfer(self, cpu):
        if self.opcode == 'MOV':
            result = self.evaluate_parameter(self.oprands[1], cpu)
            if self.oprands[0] in self.general_register.reg_list:
                self.general_register.write(self.oprands[0], result)
            elif '[' in self.oprands[0]:
                target_location = self.oprands[0].replace('[', '').replace(']', '')
                cpu.cache_memory.write(target_location, result)
        else:
            pass        


    def alu(self, cpu):
        if self.opcode == 'ADD':
            self.oprands[1] = self.evaluate_parameter(self.oprands[1], cpu)
            result = int(self.general_register.read(self.oprands[0])) + self.oprands[1]
            self.general_register.write(self.oprands[0], result)

        elif self.opcode == 'SUB':
            self.oprands[1] = self.evaluate_parameter(self.oprands[1], cpu)
            result = int(self.general_register.read(self.oprands[0])) - self.oprands[1]
            self.general_register.write(self.oprands[0], result)

        elif self.opcode == 'MUL':
            multiplier = self.evaluate_parameter(self.oprands[0], cpu)
            result = multiplier * int(self.general_register.read('AX'))
            self.general_register.write('AX', result)

        elif self.opcode == 'DIV':
            divisor = self.evaluate_parameter(self.oprands[0], cpu)
            divident = int(self.general_register.read('AX'))
            quotient = divident // divisor
            remainder = divident % divisor
            self.general_register.write('AX', quotient)
            self.general_register.write('DX', remainder)
        
        elif self.opcode == 'INC':
            result = int(self.general_register.read(self.oprands[0])) + 1
            self.general_register.write(self.oprands[0], result)

        elif self.opcode == 'DEC':
            result = int(self.general_register.read(self.oprands[0])) - 1
            self.general_register.write(self.oprands[0], result)

        else:
            sys.exit("operation code not support")


    def alu_bit(self, cpu):
        pass

    def program_transfer(self, cpu):
        if self.opcode == 'JMP':
            self.oprands[0] = self.evaluate_parameter(self.oprands[0], cpu)
            cpu.bus_interface_unit.program_counter = self.oprands[0]
        else:
            pass

    def string_operation(self, cpu):
        pass