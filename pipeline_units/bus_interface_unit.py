import sys
import queue
import time
import pprint


class bus_interface_unit(object):

    def __init__(self, instruction_queue_size, program_counter, cache_memory, special_register):
        # 预取指令队列
        self.instruction_queue = queue.Queue(instruction_queue_size) # Prefetch input queue
        self.program_counter = program_counter
        self.cache_memory = cache_memory
        self.special_register = special_register

    def run(self):
        # print()
        # print(self.instruction_queue.qsize())
        # print(self.instruction_queue.maxsize)
        
        # print(self.program_counter)
        # print("--------------------")
        # print(self.cache_memory.read_cache_location(self.program_counter))
        # print(self.cache_memory.read_single_location(0))

        # 模仿8086取指机制，queue中少了2条及以上指令便取指
        if self.instruction_queue.qsize() <= self.instruction_queue.maxsize - 2:
            self.fill_instruction_queue()
    
    def flush_pipeline(self):
        # 有分支时刷新pipeline
        self.instruction_queue.queue.clear()

    def remain_instruction(self):
        # 判断cache中是否有需要执行的指令
        return not self.cache_memory.is_null_space(self.program_counter)

    def fetch_one_instruction(self):
        # 取单条指令
        instruction = self.cache_memory.read_cache_location(self.program_counter)
        self.instruction_queue.put(instruction)
        self.program_counter += 1
        print("fetch 1 ins to queue")
        print("pipeline:")
        pprint.pprint(list(self.instruction_queue.queue))
        print()

    def fill_instruction_queue(self):
        print("filling pipeline...")
        while not self.instruction_queue.full():
            time.sleep(0.2)
            if not self.cache_memory.is_null_space(self.program_counter):
                self.fetch_one_instruction()
            else:
                break
    
