import re
import sys
import queue
from emulator.assembler import Assembler
from emulator.memory import Memory
from emulator.pipeline_units import bus_interface_unit, execution_unit
from emulator.cpu import CPU

INSTRUCTION_QUEUE_SIZE = 6
MEMORY_SIZE = int('FFFFF', 16)  # 内存空间大小 1MB
CACHE_SIZE = int('10000', 16)  # 缓存大小 64KB
SEGMENT_SIZE = int('10000', 16) # 段长度均为最大长度64kB（10000H）

DS_START = int('2000', 16) # Initial value of data segment
CS_START = int('3000', 16) # Initial value of code segment
SS_START = int('5000', 16) # Initial value of stack segment
ES_START = int('7000', 16) # Initial value of extra segment



def main():
    help = '''
    Usage:
    python main.py tests/fibonacci.asm
    python main.py tests/sub_mul_div.asm nodebug
    注：fibonacci.asm 无限循环求斐波那契数
        sub_mul_div.asm 加减乘除测试
        jmp.asm 跳转命令测试
    可以参考 README.md 中支持的汇编语言自己编写程序来运行。
    '''

    if len(sys.argv) < 2:
        print(help)
        sys.exit("Parameter incorrect")
    
    if len(sys.argv) > 2 and sys.argv[2] == 'nodebug':
        DEBUG = False
    else:
        DEBUG = True

    with open(sys.argv[1], 'r', encoding='utf-8') as file:
        asm_code = file.read()
    assembler = Assembler(DS_START, CS_START, SS_START, ES_START)
    exe_file = assembler.compile(asm_code)
    memory = Memory(MEMORY_SIZE, SEGMENT_SIZE)
    memory.load(exe_file) # load code segment

    # cache = Cache_memory(CACHE_SIZE)
    # cache.space = memory.space[reg.CS:(reg.CS+SEGMENT_SIZE)]

    BIU = bus_interface_unit.bus_interface_unit(INSTRUCTION_QUEUE_SIZE, exe_file, memory, None)
    EU = execution_unit.execution_unit(BIU, None)

    cpu = CPU(BIU, EU, None)
    print("\nCPU initialized successfully.")

    while not cpu.check_done():
        cpu.iterate(debug=DEBUG)
    cpu.print_end_state()

if __name__ == "__main__":
    main()