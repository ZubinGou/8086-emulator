import sys

class General_register(object):
    # 通用寄存器
    def __init__(self, list):
        self.list = list
        self.reg_count = len(list)
        self.space = {}
        for reg_name in list:
            self.space[reg_name] = 0
        print("initialize register done:")
        print(self.space)
        print()
    
    def read(self, reg_name):
        if reg_name not in self.list:
            sys.exit("register name error")
        return self.space[reg_name]
    
    def read_int(self, reg_name):
        if reg_name not in self.list:
            sys.exit("register name error")
        return int(self.space[reg_name])
    
    def write(self, reg_name, content):
        # content is a list
        if reg_name not in self.list:
            sys.exit("register name error")
        self.space[reg_name] = content

class Register(int):

    def __new__(cls, value=0, *args, **kwargs):
        return  super(cls, cls).__new__(cls, value)

    def __str__(self):
        return "%d" % int(self)

    def __repr__(self):
        return "%d" % int(self)

    def hex(self):
        return hex(self)
    
    def bin(self):
        return bin(self)

class Flag_register(object):
    # 标志寄存器
    # 16bits的标志寄存器，其中9个比特是被使用的，另外7个比特保留未用
    def __init__(self):
        # status flags
        self.carry = 0
        self.parity = 0
        self.auxiliary = 0
        self.zero = 0
        self.sign = 0
        self.overflow = 0
        # control flags
        self.trap = 0
        self.interrupt = 0
        self.direction = 0

class Register_file(object):
    # 寄存器堆
    def __init__(self, DATA_SEGMENT, CODE_SEGMENT, STACK_SEGMENT, EXTRA_SEGMENT):
        # General Purpose Registers
        self.GR = General_register(["AX","BX","CX","DX"])
        # Segment Registers
        self.DS = Register(DATA_SEGMENT / 16)
        self.CS = Register(CODE_SEGMENT / 16)
        self.SS = Register(STACK_SEGMENT / 16)
        self.ES = Register(EXTRA_SEGMENT / 16)
        # Pointers and Index Registers
        self.SP = Register()
        self.BP = Register()
        self.SI = Register()
        self.DI = Register()
        # Control register
        self.IP = Register()
        self.FR = Flag_register()