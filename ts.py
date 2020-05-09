import re
import ast
import sys
from assembler import to_decimal

def to_int_str(matched):
    string = matched.group().strip(' ,')
    print("string = ", string)
    int_str = str(to_decimal(string))
    print("int_str = ", int_str)
    return int_str + ','

x = "dup ( 1,02h ,101B,'$   2', 'aop* ')"
y = "DUP (' 1/.adfij,iw ,efina    ')"
z = "dup(99,'H','9' )"
x = x.split()
x = ' '.join(x)
print(x)
dup_str = x.lstrip('dupDUP').strip(' ()')

def str_to_hex(string):
    string = re.sub(r"[0-9A-F]+[HhBbOo]{1}[,\s]+", to_int_str, '[' + string + ']')
    str_list =  ast.literal_eval(string)
    store_list = []
    for item in str_list:
        # print(item)
        if isinstance(item, int):
            store_list.append(hex(item))
        elif isinstance(item, str):
            for s in item:
                store_list.append(hex(ord(s)))
        else:
            sys.exit("Compile Error: str to hex")
    return store_list

a = list(range(5))

print(a)
for i, v in enumerate(a):
    if v == 3:
        a[i] = 4
print(a)

print(to_decimal(0x123))
print(to_decimal('0x123'))
print(to_decimal(hex(123)))
print(hex(to_decimal('7123h')))
print(int(0x2000))

x = Register(2333)

print(x.hex)
print(x.to_bytes(8, 'big'))
print(bin(x.high))
print(bin(x.low))
# x = 123
x = x.write_high(1)
print(x)
print(len(x))
reg = {
            # Data Register
            'AX': 0,
            'BX': 0,
            'CX': 0,
            'DX': 0,
            # Pointer Register
            'SP': 0,
            'BP': 0,
            # Index Register
            'SI': 0,
            'DI': 0
        }
print(list(reg.keys()))
print(int('0X2000', 16))
print(to_decimal('0X2000'))