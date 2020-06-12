from emulator.assembler import Assembler

SEG_INIT = {
    'DS': int('0000', 16), # Initial value of data segment
    'CS': int('1000', 16), # Initial value of code segment
    'SS': int('0000', 16), # Initial value of stack segment
    'ES': int('0000', 16) # Initial value of extra segment
}



def load_ivt(memory): # load Interrupt Vector Table
    # 0000:0000 ~ 0000:03FF 
    for i in range(256):        # 0 ~ FF
        memory.wb(i * 4, ['0x00'])      # IP
        memory.wb(i * 4 + 1, ['0x00'])
        memory.wb(i * 4 + 2, [str(hex(i % 16)) + '0'])  # CS
        memory.wb(i * 4 + 3, ['0x1' + str(hex(i // 16))[-1]])

def load_isr(memory):
    load_ivt(memory)
    print("loading ISR...")

    for i in ['0', '1', '2', '3', '4', '7c']:
        assembler = Assembler(SEG_INIT)
        with open("./tests/Interrupt/isr" + i + ".asm", 'r', encoding='utf-8') as file:
            asm_code = file.read()
        isr = assembler.compile(asm_code)
        length = isr.seg_len['CS']
        base = (int('1000', 16) << 4) + int('100', 16) * int('0x'+i, 16)
        memory.space[base : base + length] = isr.space['CS'][:length]
    # print()
    # memory.space[1000]