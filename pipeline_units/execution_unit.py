import sys
import re
from register import *
from instructions import *
from assembler import to_decimal


class execution_unit(object):

    def __init__(self, BIU):
        self.IR = []                 # 指令寄存器
        self.opcode = ''             # 操作码
        self.opd = []                # 操作数 Operands  
        self.opbyte = 2              # 默认操作字节数: 1,2,4            
        self.eo = [0] * 5            # Evaluated opds
        self.bus = BIU               # 内部总线连接BIU
        # Flag Register
        self.FR = Flag_register()
        self.reg = {
            # Data Register
            'AX': 0,
            'BX': 0,
            'CX': 0,
            'DX': 0,
            # Pointer Register
            'SP': 0,
            'BP': 0,
            # Index Register
            'SI': 0,
            'DI': 0
        }
        self.eu_regs = list(self.reg.keys()) + ['AL', 'AH', 'BL', 'BH', 'CL', 'CH', 'DL', 'DH']
        self.biu_regs = list(BIU.reg.keys()) # 'DS', 'CS', 'SS', 'ES', 'IP'

    def run(self):
        self.IR = self.bus.instruction_queue.get()
        self.opcode = self.IR[0]
        if len(self.IR) > 1:
            self.opd = self.IR[1:]
        self.__get_opbyte()

        # self.instruction_decoder()
        # self.evaluate_all_opd()
        self.control_circuit()

    def __get_opbyte(self):
        self.opbyte = 2
        for pr in self.opd:
            if pr in ['AL', 'AH', 'BL', 'BH', 'CL', 'CH', 'DL', 'DH']:
                self.opbyte = 1
        if 'PTR' in self.opd:
            self.opd.remove['PTR']
            if 'BYTE' in self.opd:
                self.opbyte = 1
                self.opd.remove('BYTE')
            elif 'WORD' in self.opd:
                self.opbyte = 2
                self.opd.remove('WORD')
            elif 'DWORD' in self.opd:
                self.opbyte = 4
                self.opd.remove('DWORD')
            else:
                sys.exit("Runtime Error: Unexpected PTR")

    def read_reg(self, reg):
        if reg in self.biu_regs:
            res = self.bus.reg[reg]
        elif reg[1] == 'H':
            res = self.reg[reg.replace('H', 'X')] >> 8 & 0xff
        elif reg[1] == 'L':
            res = self.reg[reg.replace('L', 'X')] & 0xff
        else:
            res = self.reg[reg]
        return res

    def write_reg(self, reg, num):
        print(f"writing {num} to {reg} ...")
        if reg in self.biu_regs:
            self.bus.reg[reg] = num
        elif reg[1] == 'H':
            reg = reg.replace('H', 'X')
            self.reg[reg] = self.reg[reg] & 0xff + (num << 8)
        elif reg[1] == 'L':
            reg = reg.replace('L', 'X')
            print("regs L: ", reg)
            self.reg[reg] = (self.reg[reg] & 0xff00) + num
        else:
            self.reg[reg] = num

    def get_address(self, opd):
        # 解析所有内存寻址：直接、寄存器间接、基址、变址、基址变址、相对基址变址
        adr_reg = ['BX', 'SI', 'DI', 'BP']
        seg_reg = ['DS', 'CS', 'SS', 'ES']
        par_list = [s for s in re.split('\W', opd) if s]
        address = 0
        has_seg = False 
        for par in par_list:
            if par in adr_reg:
                address += self.read_reg(par)
            elif par in seg_reg:
                address += self.read_reg(par) << 4
                has_seg = True
            else:
                address += to_decimal(par)
        if not has_seg:
            if 'BP' in par: # 存在BP时默认段寄存器为
                address += self.read_reg('SS') << 4
            else:
                address += self.read_reg('DS') << 4
        print("Get Address", hex(address), "from opd", opd)
        return address

    def __get_byte(self, opd):
        # 内存寻址 含有 '[]'
        address = self.get_address(opd)
        content = self.bus.read_byte(address)
        print("Get Byte content:", content, " from ", hex(address))
        return content
    
    def __get_word(self, opd):
        # 内存寻址 含有 '[]'
        address = self.get_address(opd)
        content = self.bus.read_word(address)
        return content

    def __get_dword(self, opd):
       # 内存寻址 含有 '[]'
        address = self.get_address(opd)
        content = self.bus.read_dword(address)
        return content
    
    def get_int(self, opd):
        # 自动获取操作数值
        # 寄存器
        if self.is_reg(opd):
            res = self.read_reg(opd)
        # 内存
        elif '[' in opd:
            if self.opbyte == 1:
                res_list = self.__get_byte(opd)
            elif self.opbyte == 2:
                res_list = self.__get_word(opd)
            elif self.opbyte == 4:
                res_list = self.__get_dword(opd)
            else:
                sys.exit("Opbyte Error")
            res = 0
            print(res_list)
            if not res_list:
                sys.exit("Empty memory space")
            for num in res_list:
                res = (res << 8) + int(num, 16)
                print("res = ", res)
        # 立即数
        else:
            res = to_decimal(opd)
        print("get_int", hex(res), "from", opd)
        return res

    def is_reg(self, opd):
        return opd in (self.eu_regs + self.biu_regs)
    
    def is_mem(self, opd):
        return '[' in opd

    def write_mem(self, loc, content):
        # 自动写入内存
        if self.opbyte == 1:
            self.bus.write_byte(loc, content)
        elif self.opbyte == 2:
            self.bus.write_word(loc, content)
        elif self.opbyte == 4:
            self.bus.write_dword(loc, content)
        else:
            sys.exit("Opbyte Error")

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
            res = self.get_int(self.opd[1])
            if self.is_reg(self.opd[0]):
                self.write_reg(self.opd[0], res)
            elif self.is_mem(self.opd[0]):
                adr = self.get_address(self.opd[0])
                self.write_mem(adr, res)

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
            pass

        elif self.opcode == 'SUB':
            result = self.eo[0] - self.eo[1]
            self.GR.write(self.opd[0], result)

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
            self.GR.write(self.opd[0], result)

        elif self.opcode == 'DEC':
            result = self.eo[0] - 1
            self.GR.write(self.opd[0], result)

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