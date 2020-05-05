import time
import pprint


class CPU(object):
    
    def __init__(self, BIU, EU):
        self.cycle_count = 0
        self.BIU = BIU
        self.EU = EU

    def iterate(self, debug=False):
        self.cycle_count += 1
        print(f"clock cycle {self.cycle_count}: fetching...")
        self.fetch_cycle()

        self.cycle_count += 1
        print(f"clock cycle {self.cycle_count}: executing...")
        self.execute_cycle()
        
        self.print_state()
        if debug:
            input("press any key to continue...")

    def fetch_cycle(self):
        # Instruction fetch cycle 取指令周期
        self.BIU.run()
        pass

    def execute_cycle(self):
        # Instruction execution cycle 执行周期
        self.EU.run()
        pass
    
    def check_done(self):
        # 检查是否无指令，结束cpu运行
        return  self.BIU.instruction_queue.empty() and \
                not self.BIU.remain_instruction()

    def print_state(self):
        # 打印运行时状态
        print()
        print("cache memory:")
        pprint.pprint(self.BIU.cache.space[:100], compact=True)
        print()
        print("pipeline:")
        pprint.pprint(list(self.BIU.instruction_queue.queue))
        print()
        print("registers:")
        print("IP: ", self.BIU.IP)
        print("IR: ", self.EU.IR)
        for reg in self.EU.GR.reg_list:
            print(f"{reg}: ", self.EU.GR.read(reg))
        print('-'*80)
    
    def print_end_state(self):
        # 打印结束状态
        print("clock ended")
        print(f"CPU ran a total of {self.cycle_count} clock cycles")