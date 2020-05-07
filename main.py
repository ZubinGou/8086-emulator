import re
import sys
import queue
from assembler import Assembler
from memory import Memory, Cache_memory
from register import Register_file
from pipeline_units import bus_interface_unit, execution_unit
from cpu import CPU

MEMORY_SIZE = int('FFFFF', 16)  # 内存空间大小
DATA_SEGMENT = int('20000', 16) # beginning of data segment
CODE_SEGMENT = int('30000', 16) # beginning of data segment
STACK_SEGMENT = int('50000', 16) # beginning of data segment
EXTRA_SEGMENT = int('70000', 16) # beginning of data segment
SEGMENT_SIZE = int('10000', 16) # 段长度均为最大长度64kB（10000H）

CACHE_SIZE = int('10000', 16)  # 缓存大小
INSTRUCTION_QUEUE_SIZE = 6


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
        sys.exit("parameter incorrect")
    
    if len(sys.argv) > 2 and sys.argv[2] == 'nodebug':
        DEBUG = False
    else:
        DEBUG = True

    print("starting...")
    
    reg = Register_file(DATA_SEGMENT, CODE_SEGMENT, STACK_SEGMENT, EXTRA_SEGMENT)
    assembler = Assembler(DATA_SEGMENT, CODE_SEGMENT, STACK_SEGMENT, EXTRA_SEGMENT)
    exe = assembler.compile(sys.argv[1])
    memory = Memory(MEMORY_SIZE, reg.CS)
    memory.load(exe) # load code segment

    cache = Cache_memory(CACHE_SIZE)
    cache.space = memory.space[reg.CS:(reg.CS+SEGMENT_SIZE)]

    BIU = bus_interface_unit.bus_interface_unit(INSTRUCTION_QUEUE_SIZE, reg, cache, memory)
    EU = execution_unit.execution_unit(reg, BIU)

    cpu = CPU(BIU, EU)
    print("CPU initialized successfully.")

    while not cpu.check_done():
        cpu.iterate(debug=DEBUG)
    cpu.print_end_state()

if __name__ == "__main__":
    main()