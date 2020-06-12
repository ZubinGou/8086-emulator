;ALP to find the Greatest Common Deviser of two unsigned integer.
NAME Comprehensive
TITLE gcd_two
;test passed
ASSUME CS:CODE,DS:DATA

DATA SEGMENT
    NUM1 DW 0017H
    NUM2 DW 0007H
    GCD DW ?
DATA ENDS

CODE SEGMENT

START: MOV AX,DATA
       MOV DS,AX
       MOV AX,NUM1
       MOV BX,NUM2


X1:    CMP AX,BX
       JE X4
       JB X3


X2:    MOV DX,0000H
       DIV BX
       CMP DX,0000H
       JE X4
       MOV AX,DX
       JMP X1


X3:    XCHG AX,BX
       JMP X2


X4:    MOV GCD ,BX
       OUT 0,BX
       MOV AH,4CH
       INT 21H

CODE ENDS
END START