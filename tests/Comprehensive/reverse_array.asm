; 8086 ASSEMBLY PROGRAMS TO FIND REVERSE OF AN ARRAY
NAME Comprehensive
TITLE reverse_array

ASSUME CS:CODE, DS:DATA

DATA SEGMENT
    STR1 DB 01H,02H,05H,03H,04H
    STR2 DB 5 DUP(?)
DATA ENDS
 
CODE SEGMENT
    START:
            MOV AX, DATA
            MOV DS, AX
            LEA SI, STR1
            LEA DI, STR2+4
            MOV CX, 05H
    
    BACK:   CLD
            MOV AL, [SI]
            MOV [DI], AL
            INC SI
            DEC DI
            DEC CX
            JNZ BACK
    
            INT 3
CODE ENDS
END START
