
data_transfer_ins = ['MOV', 'XCHG', 'LEA', 'LDS', 'LES']
arithmetic_ins = ['ADD', 'ADC', 'SUB', 'SBB', 'INC', 'DEC', 'MUL', 'IMUL', 'DIV', 'IDIV', 'INC', 'DEC', 'CBW', 'CWD']
logical_ins = ['AND', 'OR', 'XOR', 'NOT', 'NEG', 'CPM', 'TEST']
rotate_shift_ins = ['RCL', 'RCR', 'ROL', 'ROR', 'SAL', 'SHL', 'SAR', 'SHR'] 
transfer_control_ins = ['LOOP', 'LOOPE', 'LOOPNE', 'LOOPNZ', 'LOOPZ', 'CALL', 'RET', 'RETF', 'JMP', 'JA', 'JAE', 'JB', 'JBE', 'JC', 'JCE', 'JCXZ', 'JE', 'JG', 'JGE' 'JL', 'JLE', 'JNA', 'JNAE', 'JNB', 'JNBE', 'JNC', 'JNE', 'JNG', 'JNE', 'JNG', 'JNGE', 'JNL', 'JNLE', 'JNO', 'JNP', 'JNS', 'JNZ', 'JO', 'JP', 'JPE', 'JPO', 'JS', 'JZ']
string_manipulation_ins = ['MOVSB', 'MOVSW', 'CMPSB', 'CMPSW', 'LODSB', 'LODSW', 'STOSB', 'STOSW', 'SCASB', 'SCASW', 'REP', 'REPE', 'REPZ', 'REPNE', 'REPNZ']
flag_manipulation_ins = ['STC', 'CLC', 'CMC', 'STD', 'CLD', 'STI', 'CLI', 'LANF', 'SANF']
stack_related_ins = ['PUSH', 'POP', 'PUSHF', 'POPF']
input_output_ins = ['IN', 'OUT']
miscellaneous_ins = ['NOP', 'INT', 'IRET', 'XLAT', 'HLT', 'ESC', 'INTO', 'LOCK', 'WAIT']


conditional_jump_ins = [ 'JA', 'JAE', 'JB', 'JBE', 'JC', 'JCE', 'JCXZ', 'JE', 'JG', 'JGE' 'JL', 'JLE', 'JNA', 'JNAE', 'JNB', 'JNBE', 'JNC', 'JNE', 'JNG', 'JNE', 'JNG', 'JNGE', 'JNL', 'JNLE', 'JNO', 'JNP', 'JNS', 'JNZ', 'JO', 'JP', 'JPE', 'JPO', 'JS', 'JZ']
all_ins = data_transfer_ins + arithmetic_ins + logical_ins + rotate_shift_ins + transfer_control_ins + \
          string_manipulation_ins + flag_manipulation_ins + stack_related_ins + input_output_ins + miscellaneous_ins