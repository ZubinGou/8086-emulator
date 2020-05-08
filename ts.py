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


# def pythonReSubDemo():
#     inputStr = "hello 123 world 456"
#     replacedStr = re.sub("(?P<number>\d+)", _add111, inputStr)
#     print("replacedStr=",replacedStr)#hello 234 world 567

# def _add111(matched):
#     print(matched.group())
#     intStr = matched.group("number") #123
#     intValue = int(intStr)
#     addedValue = intValue + 111         #234
#     addedValueStr = str(addedValue)
#     return addedValueStr

# if __name__=="__main__":
#     pythonReSubDemo()

a = list(range(5))

print(a)
for i, v in enumerate(a):
    if v == 3:
        a[i] = 4
print(a)