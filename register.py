import sys

class Register(object):
    # 通用寄存器和特殊寄存器
    def __init__(self, reg_list):
        self.reg_list = reg_list
        self.reg_count = len(reg_list)
        self.space = {}
        for reg_name in reg_list:
            self.space[reg_name] = 0
        print("initialize register done:")
        print(self.space)
    
    def read(self, reg_name):
        if reg_name not in self.reg_list:
            sys.exit("register name error")
        return self.space[reg_name]
    
    def write(self, reg_name, content):
        # content is a list
        if reg_name not in self.reg_list:
            sys.exit("register name error")
        self.space[reg_name] = content

class Flag_register(object):
    # 标志寄存器
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