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
        self.bus.reg['IP'] += 1
        if len(self.IR) > 1:
            self.opd = self.IR[1:]
        self.__get_opbyte()
        self.control_circuit()

    def __get_opbyte(self):
        self.opbyte = 2
        for pr in self.opd:
            if pr in ['AL', 'AH', 'BL', 'BH', 'CL', 'CH', 'DL', 'DH']:
                self.opbyte = 1
        if 'PTR' in self.opd:
            self.opd.remove('PTR')
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
            res = (self.reg[reg.replace('H', 'X')] >> 8) & 0xff
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
            self.reg[reg] = (self.reg[reg] & 0xff) + (num << 8)
        elif reg[1] == 'L':
            reg = reg.replace('L', 'X')
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

    def get_offset(self, opd):
        # 解析所有内存寻址：直接、寄存器间接、基址、变址、基址变址、相对基址变址
        # lea 0x3412:0x34; lea [si+bx]; lea 0x12; lea ss:offset; lea [bx][di]
        adr_reg = ['BX', 'SI', 'DI', 'BP']
        seg_reg = ['DS', 'CS', 'SS', 'ES']
        opd = opd.split(':')[-1] # 去掉段前缀
        par_list = [s for s in re.split('\W', opd) if s]
        offset = 0
        for par in par_list:
            if par in adr_reg:
                offset += self.read_reg(par)
            elif par in seg_reg:
                pass
            else:
                offset += to_decimal(par)
        return offset

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
        # 若opd为int也作为地址访问
        if isinstance(opd, int):
            opd = '[' + str(opd) + ']'
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

    def put_int(self, opd, num):
        # 自动将num存储到opd（寄存器或者存储器）
        if self.is_reg(opd):
            self.write_reg(opd, num)
        elif self.is_mem(opd):
            adr = self.get_address(opd)
            self.write_mem(adr, num)

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
            self.put_int(self.opd[0], res)

        elif self.opcode == 'XCHG':
            res1 = self.get_int(self.opd[0])
            res2 = self.get_int(self.opd[1])
            self.put_int(self.opd[0], res2)
            self.put_int(self.opd[1], res1)

        elif self.opcode == 'LEA':
            adr = self.get_offset(self.opd[1])
            self.put_int(self.opd[0], adr)

        elif self.opcode == 'LDS':
            adr = self.get_address(self.opd[1])
            self.write_reg(self.opd[0], self.get_int(adr))
            self.write_reg('DS', self.get_int(adr + 2))

        elif self.opcode == 'LES':
            adr = self.get_address(self.opd[1])
            self.write_reg(self.opd[0], self.get_int(adr))
            self.write_reg('ES', self.get_int(adr + 2))
        else:
            pass        

    def arithmetic_ins(self):
        if self.opcode == 'ADD':
            res1 = self.get_int(self.opd[0])
            res2 = self.get_int(self.opd[1])
            self.put_int(self.opd[0], res1 + res2)

        elif self.opcode == 'SUB':
            res1 = self.get_int(self.opd[0])
            res2 = self.get_int(self.opd[1])
            self.put_int(self.opd[0], res1 - res2)

        elif self.opcode == 'MUL': 
            pass

        elif self.opcode == 'DIV':
            pass
        
        elif self.opcode == 'INC':
            res1 = self.get_int(self.opd[0])
            self.put_int(self.opd[0], res1 + 1)

        elif self.opcode == 'DEC':
            res1 = self.get_int(self.opd[0])
            self.put_int(self.opd[0], res1 - 1)

        else:
            sys.exit("operation code not support")

    def logical_ins(self):
        if self.opcode == 'AND':
            res1 = self.get_int(self.opd[0])
            res2 = self.get_int(self.opd[1])
            self.put_int(self.opd[0], res1 & res2)

        elif self.opcode == 'OR':
            res1 = self.get_int(self.opd[0])
            res2 = self.get_int(self.opd[1])
            self.put_int(self.opd[0], res1 | res2)

        elif self.opcode == 'XOR':
            res1 = self.get_int(self.opd[0])
            res2 = self.get_int(self.opd[1])
            self.put_int(self.opd[0], res1 ^ res2)

        elif self.opcode == 'NOT':
            res1 = self.get_int(self.opd[0])
            self.put_int(self.opd[0], ~res1)

        elif self.opcode == 'NEG':
            res1 = self.get_int(self.opd[0])
            self.put_int(self.opd[0], ~res1 + 1)

        elif self.opcode == 'CPM':
            pass
        elif self.opcode == 'TEST':
            pass
        else:
            sys.exit("operation code not support")

    def rotate_shift_ins(self):
        if self.opcode == 'RCL':
            res1 = self.get_int(self.opd[0])
            res2 = self.get_int(self.opd[1])
            self.put_int(self.opd[0], res1 << res2)
            # TODO flags

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

    @property
    def ss_sp(self):
        return self.bus.reg['SS'] * 16 + self.reg['SP']

    def stack_related_ins(self):
        if self.opcode == 'PUSH':
            self.reg['SP'] -= 2
            self.write_mem(self.ss_sp, self.get_int(self.opd[0]))
        elif self.opcode == 'POP':
            res_list = self.bus.read_word(self.ss_sp)
            res = 0
            for num in res_list:
                res = (res << 8) + int(num, 16)
            if self.is_mem(self.opd[0]):
                ad = self.get_address(self.opd[0])
                self.write_mem(ad,res)
            elif self.is_reg(self.opd[0]):
                self.write_reg(self.opd[0], res)
            self.reg['SP'] += 2
        elif self.opcode == 'PUSHF':
            self.reg['SP'] -= 2
            self.write_mem(self.ss_sp, self.FR.get_int())
        elif self.opcode == 'POPF':
            res_list = self.bus.read_word(self.ss_sp)
            res = 0
            for num in res_list:
                res = (res << 8) + int(num, 16)
            self.FR.set_int(res)
            self.reg['SP'] += 2
        else:
            sys.exit("operation code not support")

    def transfer_control_ins(self):
        old_cs_ip = self.bus.cs_ip
        if self.opcode == 'JMP':
            # self.opbyte = 2
            if self.is_mem(self.opd[0]): # 转移地址在内存：jmp word/dword ptr [adr]
                adr = self.get_address(opd[0])
                if self.opbyte == 4:
                    self.opbyte = 2
                    self.write_reg('CS', self.get_int(adr + 2))
                self.write_reg('IP', self.get_int(adr))
            elif ':' in self.opd[0]:    # 长转移：jmp cs:ip
                self.opd = [s for s in re.split(' |:', self.opd[0]) if s]
                print(self.opd)
                self.write_reg('CS', self.get_int(self.opd[0]))
                self.write_reg('IP', self.get_int(self.opd[1]))
            else:                     # 短转移、近转移、寄存器转移 jmp ip/reg
                self.write_reg('IP', self.get_int(self.opd[0]))

        elif self.opcode == 'LOOP':
            self.reg['CX'] -= 1
            if self.reg['CX'] != 0:
                self.write_reg('IP', self.get_int(self.opd[0]))

        elif self.opcode in ['LOOPE', 'LOOPZ']:
            self.reg['CX'] -= 1
            if self.reg['CX'] != 0 and self.FR.zero == 1:
                self.write_reg('IP', self.get_int(self.opd[0]))

        elif self.opcode in ['LOOPNE', 'LOOPNZ']:
            self.reg['CX'] -= 1
            if self.reg['CX'] != 0 and self.FR.zero == 0:
                self.write_reg('IP', self.get_int(self.opd[0]))

        elif self.opcode == 'CALL':
            if self.opbyte == 4 or ':' in self.opcode[0]:
                self.reg['SP'] -= 2
                self.write_mem(self.bus.ss_sp, self.bus.reg['CS'])
            self.reg['SP'] -= 2
            self.write_mem(self.bus.ss_sp, self.bus.reg['IP'])
            self.opcode = 'JMP'
            self.control_circuit()

        elif self.opcode == 'RET':
            self.write_reg('IP', self.get_int(self.ss_sp))
            self.reg['SP'] += 2

        elif self.opcode == 'RETF':
            self.write_reg('IP', self.get_int(self.ss_sp))
            self.reg['SP'] += 2
            self.write_reg('CS', self.ss_sp)
            self.reg['SP'] += 2

        elif self.opcode in conditional_jump_ins:
            # 所有条件转移都是短转移 
            jmp_map = {
                'JA':  self.FR.carry == 0 and self.FR.zero == 0,
                'JAE': self.FR.carry == 0,
                'JB': self.FR.carry == 1,
                'JBE': self.FR.carry == 0 and self.FR.zero == 1,
                'JC': self.FR.carry == 1,
                'JCXZ': self.reg['CX'] == 0,
                'JE': self.FR.zero == 1,
                'JG': self.FR.zero == 0 and self.FR.sign == self.FR.overflow,
                'JGE': self.FR.sign == self.FR.overflow,
                'JL': self.FR.sign != self.FR.overflow,
                'JLE': self.FR.sign != self.FR.overflow or self.FR.zero == 1, 
                'JNA': self.FR.carry == 1 or self.FR.zero == 1,
                'JNAE': self.FR.carry == 1,
                'JNB': self.FR.carry == 0,
                'JNBE': self.FR.carry == 0 and self.FR.zero == 0,
                'JNC': self.FR.carry == 0,
                'JNE': self.FR.zero == 0,
                'JNG': self.FR.zero == 1 and self.FR.sign != self.FR.overflow,
                'JNGE': self.FR.sign != self.FR.overflow,
                'JNL': self.FR.sign == self.FR.overflow,
                'JNLE': self.FR.sign == self.FR.overflow and self.FR.zero == 0,
                'JNO': self.FR.overflow == 0,
                'JNP': self.FR.parity == 0,
                'JNS': self.FR.sign == 0,
                'JNZ': self.FR.zero == 0,
                'JO': self.FR.overflow == 1,
                'JP': self.FR.parity == 1,
                'JPE': self.FR.parity == 1,
                'JPO': self.FR.parity == 0,
                'JS': self.FR.sign == 1,
                'JZ': self.FR.zero == 1
            }
            if jmp_map[self.opcode]:
                self.write_reg('IP', self.get_int(self.opd[0]))

        else:
            sys.exit("operation code not support")

        print(f"old_cs_ip: {hex(old_cs_ip)}, new_cs_ip: {hex(self.bus.cs_ip)})")
        if old_cs_ip != self.bus.cs_ip:
            self.bus.flush_pipeline()

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

    # execution_unit 中的方法    
    def flag_manipulation_ins(self):
        if self.opcode == 'STC':
            self.FR.carry = 1
        elif self.opcode == 'CLC':
            self.FR.carry = 0
        elif self.opcode == 'CMC':
            self.FR.carry ^= 1
        elif self.opcode == 'STD':
            self.FR.direction = 1
        elif self.opcode == 'CLD':
            self.FR.direction = 0
        elif self.opcode == 'STI':
            self.FR.interrupt = 1
        elif self.opcode == 'CLI':
            self.FR.interrupt = 0
        elif self.opcode == 'LANF':
            self.write_reg('AH', self.FR.get_low())
        elif self.opcode == 'SANF':
            self.FR.set_low(self.read_reg('AH'))
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