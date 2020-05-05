import sys
import queue
import time
import pprint


class bus_interface_unit(object):

    def __init__(self, instruction_queue_size, register_file, cache):
        # 预取指令队列
        self.instruction_queue = queue.Queue(instruction_queue_size) # Prefetch input queue
        self.cache = cache
        self.DS = register_file.DS
        self.CS = register_file.CS
        self.SS = register_file.SS
        self.ES = register_file.ES
        self.IP = register_file.IP

    def read_cache(self, location):
        self.cache.read_cache_location(location)


    def run(self):
        # print()
        # print(self.instruction_queue.qsize())
        # print(self.instruction_queue.maxsize)
        
        # print(self.IP)
        # print("--------------------")
        # print(self.cache.read_cache_location(self.IP))
        # print(self.cache.read_single_location(0))

        # 模仿8086取指机制，queue中少了2条及以上指令便取指
        if self.instruction_queue.qsize() <= self.instruction_queue.maxsize - 2:
            self.fill_instruction_queue()
    
    def flush_pipeline(self):
        # 有分支时刷新pipeline
        self.instruction_queue.queue.clear()

    def remain_instruction(self):
        # 判断cache中是否有需要执行的指令
        return not self.cache.is_null_space(self.IP)

    def fetch_one_instruction(self):
        # 取单条指令
        instruction = self.cache.read_cache_location(self.IP)
        self.instruction_queue.put(instruction)
        self.IP += 1
        print("fetch 1 ins to queue")
        print("pipeline:")
        pprint.pprint(list(self.instruction_queue.queue))
        print()

    def fill_instruction_queue(self):
        print("filling pipeline...")
        while not self.instruction_queue.full():
            time.sleep(0.2)
            if not self.cache.is_null_space(self.IP):
                self.fetch_one_instruction()
            else:
                break
    
