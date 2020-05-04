import re
import sys
import queue
from memory import Memory, Cache_memory
from register import Register, Flag_register
from pipeline_units import bus_interface_unit, execution_unit
from cpu import CPU

MEMORY_SPACE = 1000     # 内存空间
CACHE_SPACE = 300       # 缓存大小
PROGRAM_BEGIN_LOCATION = 200  # 程序加载起始位置
PROGRAM_END_LOCATION = 499    # 程序加载结束位置
INSTRUCTION_QUEUE_SIZE = 6  # 


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
    program_location = PROGRAM_BEGIN_LOCATION
    memory = Memory(MEMORY_SPACE, PROGRAM_BEGIN_LOCATION, PROGRAM_END_LOCATION)
    memory.load(program_location, sys.argv[1])

    cache_memory = Cache_memory(CACHE_SPACE, PROGRAM_BEGIN_LOCATION, PROGRAM_END_LOCATION)
    cache_memory.space = memory.space[PROGRAM_BEGIN_LOCATION:PROGRAM_END_LOCATION]

    general_register = Register(["AX","BX","CX","DX"])
    special_register = Register(["SP", "BP", "SI", "DI"]) # TODO
    flag_register = Flag_register()

    BIU = bus_interface_unit.bus_interface_unit(INSTRUCTION_QUEUE_SIZE, program_location, cache_memory, special_register)
    EU = execution_unit.execution_unit(general_register, flag_register)

    cpu = CPU(BIU, EU)
    # print(cache_memory.space)
    # print(cache_memory.is_null_space(207))
    # print(cache_memory.is_null_space(208))
    while not cpu.check_done():
        cpu.iterate(debug=DEBUG)
    cpu.print_end_state()

if __name__ == "__main__":
    main()