import sys
from assembler import assemble

class Memory(object):

    def __init__(self, max_space, program_begin_location, program_end_location):
        self.max_space = max_space
        self.space = [[0] for _ in range(self.max_space)] 
        # pythonic: self.space = [[0]] * self.max_space
        self.program_begin_location = program_begin_location
        self.program_end_location = program_end_location

    def is_program_location(self, location):
        if location < self.program_begin_location or location > self.program_end_location:
            return False
        return True

    def read_single_location(self, location):
        if not self.is_program_location(location):
            sys.exit("Memory Overflow")
        return self.space[location]
    
    def write_single_location(self, location, content):
        # content is a dictionary
        if not self.is_program_location(location):
            return sys.exit("Memory Overflow")
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

class Cache_memory(Memory):
    # 高速缓存
    def __init__(self, max_space, program_begin_location, program_end_location):
        super(Cache_memory, self).__init__(max_space, 0, max_space)
        self.offset = program_begin_location

    def read_cache_location(self, location):
        return self.read_single_location(location-self.offset)

    def is_null_space(self, location):
        return self.read_single_location(location-self.offset) == [0]