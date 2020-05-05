import sys
from assembler import assemble

class Memory(object):

    def __init__(self, max_space, CS):
        self.max_space = max_space
        self.space = [[0] for _ in range(self.max_space)] 
        # pythonic: self.space = [[0]] * self.max_space
        self.program_begin = CS
        self.program_end = CS + int('10000', 16)
        print(self.program_begin)
        print(self.program_end)
        print

    def is_program_location(self, location):
        if location < self.program_begin or location > self.program_end:
            return False
        return True

    def read_single_location(self, location):
        if not self.is_program_location(location):
            sys.exit(f"Memory Overflow when reading {location}")
        return self.space[location]
    
    def write_single_location(self, location, content):
        # content is a dictionary
        if not self.is_program_location(location):
            return sys.exit(f"Memory Overflow when writing {location}")
        self.space[location] = content

    def load(self, location, file_name):
        # 加载器
        print("loading assembly code to memory...")
        instructions = assemble(file_name)
        if not self.is_program_location(location) or\
           not self.is_program_location(location+len(instructions)):
            return sys.exit("Memory Overflow")
        self.space[location:location+len(instructions)] = list(instructions) 
        # or instructions[:] or instructions.copy()
        # print(self.space)
        print("successfully loaded!")
        print()

    def load_CS(self, file_name):
        self.load(self.program_begin, file_name)

    def read_seg(self, segment_reg, offset):
        address = segment_reg * 16 + offset
        return self.read_single_location(address)

    def write_seg(self, segment_reg, offset, content):
        address = segment_reg * 16 + offset
        self.write_single_location(address, content)

class Cache_memory(Memory):
    # 高速缓存
    def __init__(self, max_space, CS):
        super(Cache_memory, self).__init__(max_space, 0)
        self.offset = 0

    def read_cache_location(self, location):
        return self.read_single_location(location-self.offset)

    def is_null_space(self, location):
        return self.read_single_location(location-self.offset) == [0]