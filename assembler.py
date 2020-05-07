import re
import os
import sys
from instructions import all_ins

data_def_ins = ['DB', 'DW', 'DD', 'DQ', 'DT', 'DUP']


def to_decimal(num):
    # all kinds of string of num to decimal
    if num[-1] == 'B':
        res = int(num.rstrip('B'), 2)
    elif num[-1] == 'O':
        res = int(num.rstrip('O'), 8)
    elif num[-1] == 'D':
        res = int(num.rstrip('D'), 10)
    elif num[-1] == 'H':
        res = int(num.rstrip('H'), 16)
    else:
        res = int(num)
    return res

class Assembler(object):
    # 汇编器 Actually It's an Interpreter :)
    def __init__(self, ds_adr, cs_adr, ss_adr, es_adr):
        self.name = ''
        self.title = ''
        self.space = {}
        self.seg_adr = {'DS': ds_adr/16, 'CS': cs_adr/16, 'SS': ss_adr/16, 'ES': es_adr/16}
        self.seg_id = {}
        self.tags = {} # 标号
        self.vars = {} # 变量
        self.ip = 0

    def compile(self, file_name):
        instructions = self.preprocessing(file_name)
        for ip in range(len(instructions)):
            ins = instructions[ip]
            if ins[0] == 'NAME':
                self.name = ins[1]
            elif ins[0] == 'TITLE':
                self.title = ins[1]
            elif ins[0] == 'ASSUME': # ASSUME必须在段之前
                self.__assume(ins[1:])
            elif len(ins) > 1 and ins[1] == 'SEGMENT':
                ip = self.__segment(instructions, ip)
        for key, val in self.space.items():
            print(key,':\n', val[:20])
            print()
        print(self.tags)
        sys.exit(0)
        return self

    def __segment(self, instructions, ip):
        seg_ip = 0
        seg_ins = instructions[ip]
        seg_tmp = seg_ins[0]
        seg_name = self.seg_id[seg_tmp] # CS DS SS ES
        self.space[seg_name] = [0] * int('10000', 16)
        for i in range(ip+1, len(instructions)):
            ins = instructions[i]
            if ins[0] == 'ORG':
                seg_ip = to_decimal(ins[1])
            elif ins[0] == 'EVEN': # 下面的内存变量从下一个偶地址单元开始分配
                seg_ip += seg_ip % 2
            elif ins[0] == 'ALIGN':
                num = to_decimal(ins[1])
                if num & (num-1): # num为2的幂
                    sys.exit("Compile Error: ALIGN num not 2's power.")
                else:
                    seg_ip += (-seg_ip) % num 
            elif ins[0] == seg_tmp:
                if ins[1] == 'ENDS':
                    return i + 1
                else:
                    sys.exit("Compile Error: segment ends fault")

            elif ':' in ins[0]: # 数据标号
                tag_list = ins[0].split(':')
                tag = tag_list[0]
                self.tags[tag] = {'seg': self.seg_adr[seg_name],
                                  'offset': seg_ip,
                                  'type': 0} # unknown type TODO
                if len(ins) == 1:                   # case1: start:\n mov ...
                    pass
                else:
                    if tag_list[1]:                 # case2: start:mov ...
                        ins[0] = tag_list[1] # 去掉标号
                    else:                           # case3: start: mov ... 
                        ins = ins[1:] # 去掉标号
                    self.space[seg_name][seg_ip] = ins
                    seg_ip += 1
            
            elif ins[0] in data_def_ins: # 数据定义伪指令
                seg_ip = self.__data_define(ins, seg_name, seg_ip)
            
            elif len(ins) > 3 and ins[1] in data_def_ins:
                var = ins[0]
                self.vars[var] = {'seg': self.seg_adr[seg_name],
                                  'offset': seg_ip,
                                  'type': var}      # var type TODO
                seg_ip = self.__data_define(ins[1:], seg_name, seg_ip)
            else: # 没有数据标号的汇编指令 直接送入段空间
                self.space[seg_name][seg_ip] = ins
                seg_ip += 1

    def __data_define(self, ins, seg_name, seg_ip): # TODO
        var = ins[0]
        if ins[2][:3] == 'DUP':
            times = to_decimal(ins[1])
            pass 
        if var == 'DB': # DB　’A’, ‘D’, 0Dh, ‘$’   DB　1, 3, 5, 7, 9, 11
            pass
        elif var == 'DW':
            pass
        elif var == 'DD':
            pass
        else:
            sys.exit("Compile Error")
        return seg_ip

    def __assume(self, ins):
        for i in ins:
            i = i.split(':')
            self.seg_id[i[1]] = i[0]

    def __strip_comments(self, text):
        return re.sub(r'(?m) *;.*n?', '', str(text))

    def __remove_empty_line(self, text):
        return os.linesep.join([s.strip() for s in text.splitlines() if s.strip()])

    def preprocessing(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            code = file.read()
            code = self.__strip_comments(code)
            code = self.__remove_empty_line(code)
            instructions = []
            for line in code.split(os.linesep):
                # print(line)
                instructions.append([s for s in re.split(" |,", line.strip().upper()) if s])
            for i in range(len(instructions)):
                print(instructions[i])
            print()
        return instructions