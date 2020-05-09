import sys
from assembler import Assembler

class Memory(object):

    def __init__(self, max_space, seg_size):
        self.max_space = max_space
        self.seg_size = seg_size
        self.space = [0] * self.max_space

    def is_null(self, loc):
        return self.space[loc] == 0 

    def verify(self, loc):
        # Verify valid address
        if loc < 0 or loc > self.max_space:
            sys.exit(f"Memory Overflow when reading {loc}")

    def rb(self, loc):
        self.verify(loc)
        print("Memory reading byte from", hex(loc))
        return self.space[loc]

    def wb(self, loc, content):
        # content is a list
        self.verify(loc)
        self.space[loc] = content

    # def read_word(self, loc):
    #     # 小端法 高位在高地址
    #     self.verify(loc)
    #     self.verify(loc + 1)
    #     return self.space[loc + 1] + self.space[loc]

    # def read_dword(self, loc, content):
    #     # 小端法 高位在高地址
    #     self.verify(loc)
    #     self.verify(loc + 3)
    #     return self.space[loc + 3] + self.space[loc + 2] + \
    #            self.space[loc + 1] + self.space[loc]

    # def write_word(self, loc, content_list):
    #     # 小端法 高位在高地址
    #     self.verify(loc)
    #     self.space[loc + 1] = content_list[0]
    #     self.space[loc] = content_list[1:]

    


    def load(self, exe):
        # 加载器
        print("loading assembly code to memory...")
        for seg, val in exe.space.items():
            adr = int(exe.seg_adr[seg], 16) * 16
            print(hex(adr))
            self.space[adr: adr + self.seg_size] = val
            print(self.space[adr:adr+100])

        print("successfully loaded!")
        print()


# class Cache_memory(Memory):
#     # 高速缓存
#     def __init__(self, max_space):
#         super(Cache_memory, self).__init__(max_space, 0)

#     def is_null_space(self, loc):
#         return self.read_byte(loc) == [0]