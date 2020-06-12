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
            int           ; 测试断点
            int           ; 测试断点
            LEA DI, STR2 + 4
            MOV CX, 05H
            int 03h       ; 测试断点
    BACK:   CLD
            MOV AL, [SI]
            MOV [DI], AL
            INC SI
            DEC DI
            DEC CX
            JNZ BACK
    
            INT 3
            mov ax,4c00h
            int 21h
CODE ENDS
END START