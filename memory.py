import sys
from assembler import Assembler

class Memory(object):

    def __init__(self, max_space):
        self.max_space = max_space
        self.space = [[0]] * self.max_space

    def memory_overflow(self, location):
        if location < 0 or location > self.max_space:
            return True
        return False

    def read_byte(self, location):
        if self.memory_overflow(location):
            sys.exit(f"Memory Overflow when reading {location}")
        return self.space[location]
    
    def write_byte(self, location, content):
        # content is a dictionary
        if self.memory_overflow(location):
            return sys.exit(f"Memory Overflow when writing {location}")
        self.space[location] = content

    def read_word(self, location):
        # 小端法 高位在高地址
        if self.memory_overflow(location):
            return sys.exit(f"Memory Overflow when writing {location}")
        return self.space[location + 1] + self.space[location]

    def write_word(self, location, content_list):
        # 小端法 高位在高地址
        if self.memory_overflow(location):
            return sys.exit(f"Memory Overflow when writing {location}")
        self.space[location + 1] = content_list[0]
        self.space[location] = content_list[1:]

    def load(self, exe):
        # 加载器
        for key, val in exe.space.items():
            pass

        print("loading assembly code to memory...")

        # or instructions[:] or instructions.copy()
        print("successfully loaded!")
        print()


class Cache_memory(Memory):
    # 高速缓存
    def __init__(self, max_space):
        super(Cache_memory, self).__init__(max_space, 0)

    def is_null_space(self, location):
        return self.read_byte(location) == [0]