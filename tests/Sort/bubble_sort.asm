;ALP to Sort a set of unsigned integer numbers in ascending/ descending
;order using Bubble sort algorithm.


DATA SEGMENT
    A DW 0005H, 0ABCDH, 5678H, 1234H, 0EFCDH, 45EFH
DATA ENDS

ASSUME CS:CODE,DS:DATA

CODE SEGMENT
    START: MOV AX,DATA
           MOV DS,AX
           MOV SI,0000H
           MOV BX,A[SI]
           DEC BX
       
       X2: MOV CX,BX
           MOV SI,02H
           
       X1: MOV AX,A[SI]
           INC SI
           INC SI
           CMP AX,A[SI]
           JA X3
           XCHG AX,A[SI]
           MOV A[SI-2],AX
           
       X3: LOOP X1
           DEC BX
           JNZ X2
           
           MOV AH,4CH
           INT 21H
CODE ENDS
END START
