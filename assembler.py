import re

def assemble(file_name):
    # 汇编器
    with open(file_name, 'r') as file:
        instructions = [re.split(" |,", line.strip().upper()) for line in file.readlines()]
    return instructions