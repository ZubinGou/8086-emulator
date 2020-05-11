import sys
import queue
import time
import pprint

class bus_interface_unit(object):

    def __init__(self, instruction_queue_size, exe, memory, console):
        # 预取指令队列
        self.instruction_queue = queue.Queue(instruction_queue_size) # Prefetch input queue
        self.reg = {
            'DS': int(exe.seg_adr['DS'], 16),
            'CS': int(exe.seg_adr['CS'], 16),
            'SS': int(exe.seg_adr['SS'], 16),
            'ES': int(exe.seg_adr['ES'], 16),
            'IP': int(exe.ip, 16)
        }
        self.pre_fetch_ip = self.reg['IP']

        print("Initial DS:", hex(self.reg['DS']))
        print("Initial CS:", hex(self.reg['CS']))
        print("Initial SS:", hex(self.reg['SS']))
        print("Initial ES:", hex(self.reg['ES']))
        print("Initial IP:", hex(self.reg['IP']))
        if console:
            console.appendPlainText("Initial DS: " + hex(self.reg['DS']))
            console.appendPlainText("Initial CS: " + hex(self.reg['CS']))
            console.appendPlainText("Initial SS: " + hex(self.reg['SS']))
            console.appendPlainText("Initial ES: " + hex(self.reg['ES']))
            console.appendPlainText("Initial IP: " + hex(self.reg['IP']))
        self.memory = memory # External bus to memory

    @property
    def cs_ip(self):
        return self.reg['CS'] * 16 + self.reg['IP']

    @property
    def cs_pre_ip(self):
        return self.reg['CS'] * 16 + self.pre_fetch_ip

    def read_byte(self, loc):
        return self.memory.rb(loc)
    
    def read_word(self, loc):
        return self.read_byte(loc + 1) + self.read_byte(loc)
    
    def read_dword(self, loc):
        # 返回list
        return self.read_byte(loc + 3) + self.read_byte(loc + 2) + \
               self.read_byte(loc + 1) + self.read_byte(loc)

    def write_byte(self, loc, content):
        # content可以为：int、list
        if isinstance(content, int):
            content = [hex(content)]
        elif isinstance(content, list):
            pass
        else:
            sys.exit("Error write_byte")
        self.memory.wb(loc, content)

    def write_word(self, loc, content): # little endian
        if isinstance(content, int):
            self.write_byte(loc, content & 0x0ff)
            self.write_byte(loc + 1, (content >> 8) & 0x0ff)
        else:
            sys.exit("Error write_byte")

    def write_dword(self, loc, content): # little endian
        if isinstance(content, int):
            self.write_byte(loc, content & 0x0ff) 
            self.write_byte(loc + 1, (content >> 8) & 0x0ff) 
            self.write_byte(loc + 2, (content >> 16) & 0x0ff)
            self.write_byte(loc + 3, content >> 24)
        else:
            sys.exit("Error write_byte")

    def run(self):
        # 模仿8086取指机制，queue中少了2条及以上指令便取指
        if self.instruction_queue.qsize() <= self.instruction_queue.maxsize - 2:
            self.fill_instruction_queue()
    @property
    def next_ins(self):
        # Pipeline 下一条指令
        ins_list = list(self.instruction_queue.queue)
        if ins_list:
            return ins_list[0]
        else:
            return "Pipline is emtpy."

    def flush_pipeline(self):
        # 有分支时刷新pipeline
        # print("Flushing pipeline...")
        self.instruction_queue.queue.clear()
        self.pre_fetch_ip = self.reg['IP']

    def remain_instruction(self):
        # 判断cache中是否有需要执行的指令
        return not self.memory.is_null(self.cs_pre_ip)

    def fetch_one_instruction(self):
        # 取单条指令
        instruction = self.memory.rb(self.cs_pre_ip)
        self.instruction_queue.put(instruction)
        self.pre_fetch_ip += 1
        # print("Fetching one ins to pipeline:")
        # pprint.pprint(list(self.instruction_queue.queue))
        # print()

    def fill_instruction_queue(self):
        # print("filling pipeline...")
        while not self.instruction_queue.full():
            # time.sleep(0.2)
            if not self.memory.is_null(self.cs_pre_ip):
                self.fetch_one_instruction()
            else:
                break
    
