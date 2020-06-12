import re
import sys
import queue
import getopt
from emulator.assembler import Assembler
from emulator.memory import Memory
from emulator.pipeline_units import bus_interface_unit, execution_unit
from emulator.cpu import CPU


INSTRUCTION_QUEUE_SIZE = 6
MEMORY_SIZE = int('FFFFF', 16)  # 内存空间大小 1MB
CACHE_SIZE = int('10000', 16)  # 缓存大小 64KB
SEGMENT_SIZE = int('10000', 16) # 段长度均为最大长度64kB（10000H）

SEG_INIT = {
    'DS': int('2000', 16), # Initial value of data segment
    'CS': int('3000', 16), # Initial value of code segment
    'SS': int('5000', 16), # Initial value of stack segment
    'ES': int('7000', 16) # Initial value of extra segment
}


def main():
    help = '''
    Usage:
    python main.py ./tests/Requirement/bubble_sort.asm -i
    python main.py ./tests/Interrupt/show_date_time.asm -n
    注：-i表示打印中断信息，-n表示禁用debug。tests文件夹内含有大量测试用例
    可以参考文档，自行编写汇编语言程序来运行。
    '''

    DEBUG = True  # 是否单步运行
    INT_MSG = False  # 是否打印中断信息
    try:
        opts,args = getopt.getopt(sys.argv[2:],'-h-n-i',['help','nodebug','interrupt'])
        for opt_name,opt_value in opts:
            if opt_name in ('-h','--help'):
                print(help)
                exit()
            if opt_name in ('-n', '--nodebug'):
                DEBUG = False
            if opt_name in ('-i', '--interrupt'):
                INT_MSG = True
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            asm_code = file.read()
    except:
        print(help)
        sys.exit("Parameter incorrect")
   
    assembler = Assembler(SEG_INIT)
    exe_file = assembler.compile(asm_code)
    memory = Memory(MEMORY_SIZE, SEGMENT_SIZE)
    memory.load(exe_file) # load code segment

    BIU = bus_interface_unit.bus_interface_unit(INSTRUCTION_QUEUE_SIZE, exe_file, memory)
    EU = execution_unit.execution_unit(BIU, INT_MSG)
    cpu = CPU(BIU, EU, gui_mode=False)
    print("\nCPU initialized successfully.")
    print("=" * 80)

    while not cpu.check_done():
        cpu.iterate(debug=DEBUG)
    cpu.print_end_state()

if __name__ == "__main__":
    main()